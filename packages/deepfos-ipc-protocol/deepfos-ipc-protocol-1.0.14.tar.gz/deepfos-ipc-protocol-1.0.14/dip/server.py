import asyncio
import os
import typing

from loguru import logger

from dip.utils import (
    resolve_header_protocol,
    resolve_msg_protocol,
    resolve_detaillist_protocol,
    read_len_prefix
)
from dip.const import (
    HEADER_PROTOCOL,
    MESSAGE_PROTOCOL,
    DETAILLIST_PROTOCOL,
    PROTOCOL_DEF,
    read_config
)

CURRENTPATH = os.path.dirname(__file__)


# -----------------------------------------------------------------------------
# typing
Callback_T = typing.Callable[['ServerProtocol', str, typing.Any], typing.Any]


class Stream:
    def __init__(self):
        self._pending = None
        self._ready = []

    def new_segmant(self, buf):
        buf_len = len(buf)
        expect_len = read_len_prefix(buf) + 5
        if expect_len == buf_len:
            self._ready.append(buf)
            self._pending = None
        elif expect_len > buf_len:
            self._pending = buf
        else:
            self._ready.append(buf[:expect_len])
            self._pending = buf[expect_len:]

    def amend_pending(self, buf):
        new_buf = self._pending + buf
        self.new_segmant(new_buf)

    def feed_data(self, buf: bytes):
        if not self._pending:
            self.new_segmant(buf)
        else:
            self.amend_pending(buf)

    def iter_data(self):
        while self._ready:
            yield self._ready.pop(0)


class DeepfosIPCProtocol(asyncio.Protocol):

    def __init__(self, callback: Callback_T = None, **kwargs) -> None:
        self.data = None
        self.callback = callback
        self.transport = None
        self.kwargs = kwargs
        self._stream = Stream()

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        if data == b"end":
            self.transport.write(b"end")
            self.transport.close()
            self.transport = None
            return

        self._stream.feed_data(data)

        errors = []
        data_processed = False

        for buf in self._stream.iter_data():
            data_processed = True
            try:
                self.process_message(buf)
            except Exception as e:
                logger.error(e)
                errors.append(repr(e).encode("utf8"))

        if data_processed:
            if errors:
                self.transport.write(b''.join(errors))
            else:
                self.transport.write(b"success")

    def process_message(self, data):
        mtype = data[0]
        if mtype in MESSAGE_PROTOCOL:
            self.data = resolve_msg_protocol(data)
            logger.opt(lazy=True).debug("Task Meta received: {data!r}", data=lambda: self.data)
        elif mtype in HEADER_PROTOCOL:
            self.data = resolve_header_protocol(data)
            logger.opt(lazy=True).debug("Task Meta received: {!r}".format(self.data))
        elif mtype in DETAILLIST_PROTOCOL:
            self.data = list(resolve_detaillist_protocol(data))
            logger.opt(lazy=True).debug("Task Meta received: {!r}".format(self.data))
        else:
            raise ValueError(f"Unsupported mtype: {chr(mtype)}")
        if self.callback is not None:
            self.callback(self, chr(mtype), self.data, **self.kwargs)

    def connection_lost(self, error):
        if error:
            logger.error('SERVER ERROR: {}'.format(error))
        else:
            logger.debug('Client Closed')
        super().connection_lost(error)
        self.transport = None


class Server:
    """
    启动Server服务.
    """
    def __init__(
        self,
        path: str,
        callback: Callback_T = None,
        config=PROTOCOL_DEF,
        **kwrags
    ) -> None:
        self.path = path
        self.callback = callback
        self.waiter = None
        self.kwargs = kwrags
        read_config(config)

    async def _create_server(self, loop):
        srv = await loop.create_unix_server(
            lambda: DeepfosIPCProtocol(self.callback, **self.kwargs), self.path,
        )
        return srv

    async def start(self):
        loop = asyncio.get_running_loop()
        self.waiter = loop.create_future()

        srv = await self._create_server(loop)
        async with srv:
            await srv.start_serving()
            await self.waiter
        logger.info('<Server> End of task.')

    def stop(self):
        if self.waiter is not None:
            logger.debug('Stop server.')
            self.waiter.set_result(None)
            self.waiter = None

# async def run():
#     m = MasterServer("../unix_sock.sock")
#     await m.task()

# asyncio.run(run())

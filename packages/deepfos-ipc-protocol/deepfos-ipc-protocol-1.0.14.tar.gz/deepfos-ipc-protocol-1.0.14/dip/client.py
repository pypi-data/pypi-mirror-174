import asyncio
import os
import typing

from loguru import logger

from dip.utils import (
    judge_data_format,
    to_msg_protocol,
    to_header_protocol,
    to_detaillist_protocol,
)
from dip.const import (
    HEADER_PROTOCOL,
    MESSAGE_PROTOCOL,
    DETAILLIST_PROTOCOL,
    read_config
)

CURRENTPATH = os.path.dirname(__file__)


class ClientProtocol(asyncio.Protocol):

    def __init__(self, ins):
        self.ins = ins
        self.transport = None

    def connection_made(self, transport):
        logger.debug("Connection made")
        self.transport = transport

    def data_received(self, data):
        if data == b"end":
            self.transport.close()
        if data and not self.ins.future.done():
            self.ins.future.set_result(data)
        logger.debug("Data received: {!r}".format(data.decode()))

    def connection_lost(self, error):
        if error:
            logger.error('ERROR: {}'.format(error))
        else:
            logger.debug('The server closed the connection')


class Client:
    _singleton_ins = None

    def __new__(
        cls,
        path: str = None,
        config: typing.Dict = None,
        singleton: bool = True
    ):
        if singleton:
            if cls._singleton_ins is None:
                ins = super().__new__(cls)
                ins.is_singleton = True
                ins.refcount = 1
                ins.__init__(path, config, singleton)
                cls._singleton_ins = ins
            else:
                ins = cls._singleton_ins
                ins.refcount += 1
        else:
            ins = super().__new__(cls)
            ins.refcount = 0
            ins.is_singleton = False
        return ins

    def __init__(
        self,
        path: str,
        config: typing.Dict = None,
        singleton: bool = True
    ):
        if self.__class__._singleton_ins is None:
            self.path = path
            self.transport = None
            self.future = None
            if config:
                read_config(config)
            if not HEADER_PROTOCOL:
                read_config(config)

    @staticmethod
    def _processing_data(mtype: str, data):
        """将传入的数据转为服务端可读取的数据"""
        if mtype in MESSAGE_PROTOCOL:
            buf = to_msg_protocol(mtype, data)
        elif mtype in HEADER_PROTOCOL:
            buf = to_header_protocol(mtype, data)
        elif mtype in DETAILLIST_PROTOCOL:
            buf = to_detaillist_protocol(mtype, data)
        else:
            raise ValueError("Unsupported message type: {}".format(mtype))
        return buf

    async def connect(self):
        """建立和服务端的连接"""
        loop = asyncio.get_running_loop()
        if not self.transport or self.transport.is_closing():
            transport, protocol = await loop.create_unix_connection(
                lambda: ClientProtocol(self), self.path
            )
            self.transport = transport

    async def send_msg(self, mtype, message):
        """向服务端发送数据"""
        loop = asyncio.get_running_loop()
        if self.transport and not self.transport.is_closing():
            judge_data_format(mtype, message)
            self.future = loop.create_future()
            data = self._processing_data(mtype, message)
            self.transport.write(data)
            return await self.future
        return None

    async def _close(self):
        logger.debug('close client')
        loop = asyncio.get_running_loop()
        self.future = loop.create_future()
        self.transport.write(b'end')
        await self.future
        self.transport.close()
        self.transport = None

    async def close(self):
        if self.is_singleton:
            self.refcount -= 1
            if self.refcount == 0:
                await self._close()
                self.__class__._singleton_ins = None
            else:
                logger.debug(f'Remaining clients: {self.refcount}')
        else:
            await self._close()

    async def ensure_closed(self):
        if self.transport is None or self.transport.is_closing():
            return
        await self._close()

# async def async_main():
#     m = WorkerClient("../unix_sock.sock", config="../default.json")
#     c = WorkerClient()
#     await m.create_conn() # 建立一个连接
#     await m.send_msg("O", "你好")

    # await WorkerClient.send_msg(
    #     "U", [
    #         {
    #             "key": "key",
    #             "name": "你好",
    #             "status": "status",
    #             "endTime": "endTime",
    #             "arg": "xxxx"
    #         }
    #     ]
    # )
    # await WorkerClient.send_msg(
    #     "H", {"header": "你好"}
    # )
    # await WorkerClient.send_msg(
    #     "I", [
    #         {
    #             "key": "key",
    #             "name": "name",
    #         }
    #     ]
    # )
    # await WorkerClient.send_msg(
    #     "E", "xxxss"
    # )
    # await WorkerClient.send_msg(
    #     "e", {"subtask_err": "err", "arg": "arg"}
    # )
    # await WorkerClient.send_msg(
    #     "o", {"subtask_out": "out", "arg": "arg"}
    # )
#     await m.close()
#     await c.close()
#     await c.send_msg("O", "你好2")
#     # await c.close()
#     # await c.send_msg("O", "你好3")

# asyncio.run(async_main())

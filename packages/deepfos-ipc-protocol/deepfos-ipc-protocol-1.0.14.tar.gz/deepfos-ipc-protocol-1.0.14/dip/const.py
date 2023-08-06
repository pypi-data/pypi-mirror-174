import typing

from dip.errors import UnsupportedProtocolError

HEADER_PROTOCOL = []
MESSAGE_PROTOCOL = []
DETAILLIST_PROTOCOL = []
KNOWN_PROTOCOL = set()
PROTOCOL_MAP = {}
PROTOCOL_DEF = {
    "HEADER_PROTOCOL": [
        {
            "H": ["header"]
        },
        {
            "o": ["arg", "subtask_out"]
        },
        {
            "e": ["arg", "subtask_err"]
        }
    ],
    "MESSAGE_PROTOCOL": ["O", "E"],
    "DETAILLIST_PROTOCOL": [
        {
            "I": ["key", "name"]
        },
        {
            "U": ["key", "status", "endTime", "name", "arg"]
        }
    ]
}


def set_var(headers, protocol: str):
    """设置全局变量"""
    temp_var = {}
    if protocol == 'HEADER_PROTOCOL':
        key = list(headers.keys())[0]
        ingeter = ord(key)
        HEADER_PROTOCOL.append(key)
        HEADER_PROTOCOL.append(ingeter)
        for index, value in enumerate(headers[key]):
            temp_var[bytes.fromhex(f"000{index+1}")] = value
        PROTOCOL_MAP[(key, ingeter)] = {
            "reverse": {
                v: k for k, v in temp_var.items()
            },
            "fields": temp_var
        }
    elif protocol == 'MESSAGE_PROTOCOL':
        key = headers
        ingeter = ord(key)
        MESSAGE_PROTOCOL.append(key)
        MESSAGE_PROTOCOL.append(ingeter)
    elif protocol == 'DETAILLIST_PROTOCOL':
        key = list(headers.keys())[0]
        ingeter = ord(key)
        DETAILLIST_PROTOCOL.append(key)
        DETAILLIST_PROTOCOL.append(ingeter)
        for index, value in enumerate(headers[key]):
            temp_var[bytes.fromhex(f"000{index+1}")] = value
        PROTOCOL_MAP[(key, ingeter)] = {
            "reverse": {
                v: k for k, v in temp_var.items()
            },
            "fields": temp_var
        }
    else:
        raise UnsupportedProtocolError(f"Unsupported protocol: <{protocol}>")


def read_config(config: typing.Dict[str, typing.List]):
    if config is None:
        config = PROTOCOL_DEF
    for proto_type, proto in config.items():
        for headers in proto:
            set_var(headers, proto_type)

    KNOWN_PROTOCOL.clear()
    KNOWN_PROTOCOL.update(MESSAGE_PROTOCOL + HEADER_PROTOCOL + DETAILLIST_PROTOCOL)

import base64
import socket
import sys
import types
from abc import ABCMeta, abstractmethod
from collections import Mapping, Set

import cloudpickle
from eventlet.green import zmq
from eventlet.queue import LightQueue
from msgpack import ExtType, packb, unpackb
from pyrsistent import PBag, PList, PVector, pbag, plist, pmap, pset, pvector

_native_builtin_types = (int, float, str, bool, type(None))

TYPE_PSET = 1
TYPE_PLIST = 2
TYPE_PBAG = 3
TYPE_MBOX = 4
TYPE_FUNC = 5


def decode(obj):
    if isinstance(obj, ExtType):
        if obj.code == TYPE_PSET:
            unpacked_data = unpackb(obj.data, use_list=False, encoding="utf-8")
            return pset(decode(item) for item in unpacked_data)
        if obj.code == TYPE_PLIST:
            unpacked_data = unpackb(obj.data, use_list=False, encoding="utf-8")
            return plist(decode(item) for item in unpacked_data)
        if obj.code == TYPE_PBAG:
            unpacked_data = unpackb(obj.data, use_list=False, encoding="utf-8")
            return pbag(decode(item) for item in unpacked_data)
        if obj.code == TYPE_FUNC:
            return decode_func(obj.data)
        module_name, class_name, *data = unpackb(
            obj.data, use_list=False, encoding="utf-8"
        )
        cls = getattr(sys.modules[module_name], class_name)
        if obj.code == TYPE_MBOX:
            return cls.decode(data)
        return cls(*(decode(item) for item in data))
    if isinstance(obj, tuple):
        return pvector(decode(item) for item in obj)
    if isinstance(obj, dict):
        new_dict = dict()
        for key in obj.keys():
            new_dict[decode(key)] = decode(obj[key])
        return pmap(new_dict)
    return obj


def encode(obj):
    if type(obj) in (list, tuple) or isinstance(obj, PVector):
        return [encode(item) for item in obj]
    if isinstance(obj, Mapping):
        encoded_obj = {}
        for key in obj.keys():
            encoded_obj[encode(key)] = encode(obj[key])
        return encoded_obj
    if isinstance(obj, _native_builtin_types):
        return obj
    if isinstance(obj, Set):
        return ExtType(
            TYPE_PSET, packb([encode(item) for item in obj], use_bin_type=True)
        )
    if isinstance(obj, PList):
        return ExtType(
            TYPE_PLIST, packb([encode(item) for item in obj], use_bin_type=True)
        )
    if isinstance(obj, PBag):
        return ExtType(
            TYPE_PBAG, packb([encode(item) for item in obj], use_bin_type=True)
        )
    if isinstance(obj, types.FunctionType):
        return ExtType(TYPE_FUNC, encode_func(obj))
    if isinstance(obj, Receiver):
        return ExtType(TYPE_MBOX, packb(obj.encode(), use_bin_type=True))

    cls = obj.__class__
    return ExtType(
        0,
        packb(
            [cls.__module__, cls.__name__] + [encode(item) for item in obj],
            use_bin_type=True,
        ),
    )


def decode_func(obj):
    return cloudpickle.loads(obj)


def encode_func(obj):
    return cloudpickle.dumps(obj)


class Receiver(metaclass=ABCMeta):
    @abstractmethod
    def encode(self):
        pass

    @staticmethod
    @abstractmethod
    def decode(params):
        pass


class Mailbox(Receiver, metaclass=ABCMeta):
    @abstractmethod
    def put(self, message):
        pass

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def encode(self):
        pass

    @staticmethod
    @abstractmethod
    def decode(params):
        pass

    def __ne__(self, other):
        return not self.__eq__(other)


class AckableMailbox(Mailbox, metaclass=ABCMeta):
    @abstractmethod
    def put(self, message):
        pass

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def ack(self):
        pass

    @abstractmethod
    def encode(self):
        pass

    @staticmethod
    @abstractmethod
    def decode(params):
        pass


Mailbox.register(LightQueue)


class LocalMailbox(Mailbox):
    __slots__ = ["_queue"]

    def __init__(self):
        self._queue = LightQueue()

    def put(self, message):
        self._queue.put(message)

    def get(self):
        return self._queue.get(block=True)

    def encode(self):
        raise NotImplementedError

    @staticmethod
    def decode(params):
        raise NotImplementedError


class KombuMailbox(AckableMailbox):
    __slots__ = ["_address", "_conn", "_queue", "_no_ack", "_last_msg"]

    def __init__(
        self,
        address,
        name,
        transport_options,
        ssl=False,
        no_ack=True,
        queue_opts=None,
        exchange_opts=None,
    ):
        from kombu import Connection

        self._address = address
        self._conn = Connection(address, transport_options=transport_options, ssl=ssl)
        self._queue = self._conn.SimpleQueue(name, no_ack, queue_opts, exchange_opts)
        self._no_ack = no_ack
        self._last_msg = None

    def get(self):
        self._last_msg = self._queue.get()
        return decode(unpackb(self._last_msg.body, encoding="utf-8", use_list=False))

    def put(self, message):
        return self._queue.put(
            packb(encode(message), encoding="utf-8", use_bin_type=True)
        )

    def ack(self):
        if self._no_ack:
            return
        if self._last_msg is not None:
            self._last_msg.ack()
            self._last_msg = None

    def encode(self):
        raise NotImplementedError

    @staticmethod
    def decode(params):
        raise NotImplementedError

    def __enter__(self):
        return self

    def __exit__(self, *exc_details):
        self.__del__()

    def __del__(self):
        if hasattr(self, "_queue"):
            self._queue.close()
        if hasattr(self, "_conn"):
            self._conn.close()

    def __str__(self):
        return self._address

    def __eq__(self, other):
        return self.__class__ is other.__class__ and self._address == other._address


class SQSMailbox(AckableMailbox):
    __slots__ = ["_name", "_queue", "_last_msg", "_last_msgs", "_no_ack"]

    def __init__(self, name, no_ack=True):
        import boto3

        sqs = boto3.resource("sqs")
        self._name = name
        self._queue = sqs.get_queue_by_name(QueueName=name)
        self._last_msg = None
        self._last_msgs = None
        self._no_ack = no_ack

    def get(self, **kwargs):
        while self._last_msgs is None or len(self._last_msgs) == 0:
            self._last_msgs = self._queue.receive_messages(**kwargs)
        self._last_msg = self._last_msgs.pop(0)
        if self._no_ack:
            self._last_msg.delete()
        return decode(
            unpackb(
                base64.decodebytes(bytes(self._last_msg.body, "utf-8")),
                encoding="utf-8",
                use_list=False,
            )
        )

    def put(self, message, **kwargs):
        return self._queue.send_message(
            MessageBody=str(
                base64.encodebytes(
                    packb(encode(message), encoding="utf-8", use_bin_type=True)
                ),
                "utf-8",
            ),
            **kwargs
        )

    def ack(self):
        if self._no_ack:
            return
        if self._last_msg is not None:
            self._last_msg.delete()
            self._last_msg = None

    def encode(self):
        cls = self.__class__
        return [cls.__module__, cls.__name__, self._name, self._no_ack]

    @staticmethod
    def decode(params):
        name, no_ack = params
        return SQSMailbox(name, no_ack=no_ack)

    def __enter__(self):
        return self

    def __exit__(self, *exc_details):
        self.__del__()

    def __del__(self):
        pass

    def __str__(self):
        return str(self._queue.url)

    def __eq__(self, other):
        return self.__class__ is other.__class__ and self._queue.url == other._queue.url

    def __hash__(self):
        return hash(self._queue.url)


class ZmqInbox(Mailbox):
    __slots__ = ["_url", "_context", "_recv_sock"]

    def __init__(self, url="tcp://*:9999", **kwargs):
        self._url = url
        self._context = zmq.Context(**kwargs)
        self._recv_sock = self._context.socket(zmq.PULL)
        self._recv_sock.bind(url)

    def get(self):
        return decode(unpackb(self._recv_sock.recv(), encoding="utf-8", use_list=False))

    def put(self, message):
        raise NotImplementedError()

    def encode(self):
        raise NotImplementedError

    @staticmethod
    def decode(params):
        raise NotImplementedError

    def __enter__(self):
        return self

    def __exit__(self, *exc_details):
        self.__del__()

    def __del__(self):
        self._recv_sock.close()

    def __str__(self):
        return self._url

    def __eq__(self, other):
        return self.__class__ is other.__class__ and self._url == other._url

    def __hash__(self):
        return hash(self._url)


class ZmqOutbox(Mailbox):
    __slots__ = ["_url", "_context", "_send_sock"]

    def __init__(self, url, **kwargs):
        self._url = url
        self._context = zmq.Context(**kwargs)
        self._send_sock = self._context.socket(zmq.PUSH)
        self._send_sock.connect(self._url)

    def get(self):
        raise NotImplementedError()

    def put(self, msg):
        self._send_sock.send(packb(encode(msg), encoding="utf-8", use_bin_type=True))

    def encode(self):
        raise NotImplementedError

    @staticmethod
    def decode(params):
        raise NotImplementedError

    def __enter__(self):
        return self

    def __exit__(self, *exc_details):
        self.__del__()

    def __del__(self):
        self._send_sock.close()

    def __str__(self):
        return self._url

    def __eq__(self, other):
        return self.__class__ is other.__class__ and self._url == other._url

    def __hash__(self):
        return hash(self._url)


def get_hostname():
    return socket.getfqdn()


class TcpInbox(Mailbox):
    __slots__ = ["_port", "_url", "_context", "_recv_sock"]

    def __init__(self, port=9999, **kwargs):
        self._port = port
        self._url = "tcp://*:" + str(port)
        self._context = zmq.Context(**kwargs)
        self._recv_sock = self._context.socket(zmq.PULL)
        self._recv_sock.bind(self._url)

    def get(self):
        return decode(unpackb(self._recv_sock.recv(), encoding="utf-8", use_list=False))

    def put(self, message):
        raise NotImplementedError()

    def encode(self):
        cls = self.__class__
        return [cls.__module__, cls.__name__, get_hostname(), self._port]

    @staticmethod
    def decode(params):
        address, port = params
        return TcpOutbox(address, port)

    def __enter__(self):
        return self

    def __exit__(self, *exc_details):
        self.__del__()

    def __del__(self):
        self._recv_sock.close()
        self._context.term()

    def __str__(self):
        return self._url

    def __eq__(self, other):
        return self.__class__ is other.__class__ and self._url == other._url

    def __hash__(self):
        return hash(self._url)


class TcpOutbox(Mailbox):
    __slots__ = ["_url", "_context", "_send_sock"]

    def __init__(self, address, port, **kwargs):
        self._url = "tcp://" + address + ":" + str(port)
        self._context = zmq.Context(**kwargs)
        self._send_sock = self._context.socket(zmq.PUSH)
        self._send_sock.connect(self._url)

    def get(self):
        raise NotImplementedError()

    def put(self, msg):
        self._send_sock.send(packb(encode(msg), encoding="utf-8", use_bin_type=True))

    def encode(self):
        raise NotImplementedError

    @staticmethod
    def decode(params):
        raise NotImplementedError

    def __enter__(self):
        return self

    def __exit__(self, *exc_details):
        self.__del__()

    def __del__(self):
        self._send_sock.close()
        self._context.term()

    def __str__(self):
        return self._url

    def __eq__(self, other):
        return self.__class__ is other.__class__ and self._url == other._url

    def __hash__(self):
        return hash(self._url)


class IpcInbox(Mailbox):
    __slots__ = ["_port", "_url", "_context", "_recv_sock"]

    def __init__(self, address, **kwargs):
        self._url = "ipc://" + address
        self._context = zmq.Context(**kwargs)
        self._recv_sock = self._context.socket(zmq.PULL)
        self._recv_sock.bind(self._url)

    def get(self):
        return decode(unpackb(self._recv_sock.recv(), encoding="utf-8", use_list=False))

    def put(self, message):
        raise NotImplementedError()

    def encode(self):
        cls = self.__class__
        return [cls.__module__, cls.__name__, self._url]

    @staticmethod
    def decode(params):
        return IpcOutbox(params[0])

    def __enter__(self):
        return self

    def __exit__(self, *exc_details):
        self.__del__()

    def __del__(self):
        self._recv_sock.close()
        self._context.term()

    def __str__(self):
        return self._url

    def __eq__(self, other):
        return self.__class__ is other.__class__ and self._url == other._url

    def __hash__(self):
        return hash(self._url)


class IpcInboxR(Mailbox):
    __slots__ = ["_port", "_url", "_context", "_recv_sock"]

    def __init__(self, address, zmq_context=zmq.Context.instance()):
        self._url = "ipc://" + address
        self._context = zmq_context
        self._recv_sock = self._context.socket(zmq.PULL)
        self._recv_sock.connect(self._url)

    def get(self):
        return decode(unpackb(self._recv_sock.recv(), encoding="utf-8", use_list=False))

    def put(self, message):
        raise NotImplementedError()

    def encode(self):
        raise NotImplementedError()

    @staticmethod
    def decode(params):
        raise NotImplementedError()

    def __enter__(self):
        return self

    def __exit__(self, *exc_details):
        self.__del__()

    def __del__(self):
        self._recv_sock.close()
        self._context.term()

    def __str__(self):
        return self._url

    def __eq__(self, other):
        return self.__class__ is other.__class__ and self._url == other._url

    def __hash__(self):
        return hash(self._url)


class IpcOutbox(Mailbox):
    __slots__ = ["_url", "_context", "_send_sock"]

    def __init__(self, address, **kwargs):
        self._url = "ipc://" + address
        self._context = zmq.Context(**kwargs)
        self._send_sock = self._context.socket(zmq.PUSH)
        self._send_sock.connect(self._url)

    def get(self):
        raise NotImplementedError()

    def put(self, msg):
        self._send_sock.send(packb(encode(msg), encoding="utf-8", use_bin_type=True))

    def encode(self):
        raise NotImplementedError

    @staticmethod
    def decode(params):
        raise NotImplementedError

    def __enter__(self):
        return self

    def __exit__(self, *exc_details):
        self.__del__()

    def __del__(self):
        self._send_sock.close()
        self._context.term()

    def __str__(self):
        return self._url

    def __eq__(self, other):
        return self.__class__ is other.__class__ and self._url == other._url

    def __hash__(self):
        return hash(self._url)


class IpcOutboxR(Mailbox):
    __slots__ = ["_url", "_context", "_send_sock"]

    def __init__(self, address, zmq_context=zmq.Context.instance()):
        self._url = "ipc://" + address
        self._context = zmq_context
        self._send_sock = self._context.socket(zmq.PUSH)
        self._send_sock.bind(self._url)

    def get(self):
        raise NotImplementedError()

    def put(self, msg):
        self._send_sock.send(packb(encode(msg), encoding="utf-8", use_bin_type=True))

    def encode(self):
        raise NotImplementedError

    @staticmethod
    def decode(params):
        raise NotImplementedError

    def __enter__(self):
        return self

    def __exit__(self, *exc_details):
        self.__del__()

    def __del__(self):
        self._send_sock.close()
        self._context.term()

    def __str__(self):
        return self._url

    def __eq__(self, other):
        return self.__class__ is other.__class__ and self._url == other._url

    def __hash__(self):
        return hash(self._url)

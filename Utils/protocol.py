import enum


class Protocol(enum.Enum):
    PING = 0
    PONG = 1
    EXIT = 2
    ID = 3
    START = 4
    WIN = 5
    LOSE = 6
    PENGUIN = 7
    WALL = 8


class Message:
    def __init__(self, protocol: Protocol, data: str):
        self.data = data
        self.protocol = protocol

    def to_bytes(self) -> bytes:
        return bytes([self.protocol.value]) + self.data.encode("UTF-8")

    @classmethod
    def from_bytes(cls, data: bytes):
        protocol = Protocol(data[0])
        return cls(protocol, data[1:].decode("UTF-8"))

    def __str__(self):
        return f'{self.protocol.name} {self.data}'

    def __repr__(self):
        return str(self)

"""
### About
- This module defines the communication protocol between the client and server.
- It contains an enumeration of the available protocols 
and a class to encapsulate messages.
"""
import enum


class Protocol(enum.Enum):
    """
    ### About
    - This enumeration defines the available communication protocols.
    ### Available Protocols
    - `PING`: A protocol used to check if the connection is still active.
    - `PONG`: A protocol used to respond to a `PING` request.
    - `EXIT`: A protocol used to close the connection.
    - `ID`: A protocol used to send the client's id.
    - `START`: A protocol used to start the game.
    - `WIN`: A protocol used to signal a win.
    - `LOSE`: A protocol used to signal a loss.
    - `PENGUIN`: A protocol used to signal a move regarding the penguin.
    - `WALL`: A protocol used to signal a move regarding the wall.
    """
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
    """
    ### About
    - This class is used to encapsulate data sent between the client and server.
    ### Methods
    - `to_bytes`: Converts the message to bytes.
    - `from_bytes`: Converts bytes to a message.
    ### Attributes
    - `data`: The data to be sent.
    - `protocol`: The protocol used to send the data.
    """
    def __init__(self, protocol: Protocol, data: str):
        """
        ### About
        - This method initializes the message.
        ### Parameters
        - `protocol`: The protocol used to send the data.
        - `data`: The data to be sent
        """
        self.data = data
        self.protocol = protocol

    def to_bytes(self) -> bytes:
        """
        ### About
        - This method converts the message to bytes.
        ### Returns
        - The message as bytes.
        """
        return bytes([self.protocol.value]) + self.data.encode("UTF-8")

    @classmethod
    def from_bytes(cls, data: bytes):
        """
        ### About
        - This method converts bytes to a message.
        ### Parameters
        - `data`: The bytes to be converted.
        ### Returns
        - The message.
        """
        protocol = Protocol(data[0])
        return cls(protocol, data[1:].decode("UTF-8"))

    def __str__(self):
        return f'{self.protocol.name} {self.data}'

    def __repr__(self):
        return str(self)

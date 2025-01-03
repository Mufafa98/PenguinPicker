"""
### About
- This module defines basic utilities used by the client and server.
### Available Classes
- `Protocol`: An enumeration of the available comunication protocols.
- `Message`: A class used to encapsulate data sent between the client
and server.
### Available Constants
- `SERVER_IP`: The IP address of the server.
- `SERVER_PORT`: The port used by the server.
"""

from .protocol import Protocol
from .protocol import Message

SERVER_IP = 'localhost'
"""The IP address of the server."""
SERVER_PORT = 9898
"""The port used by the server."""

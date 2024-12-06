import socket


class IdTool:

    def __init__(self):
        self._connected_clients = dict()
        self._available_ids = list()
        self._counter = 0

    def connect(self, client_socket: socket.socket) -> int:
        if self._available_ids == []:
            self._connected_clients[client_socket] = self._counter
            self._counter += 1
            return self._counter - 1
        else:
            new_id = self._available_ids.pop(0)
            self._connected_clients[client_socket] = new_id
            return new_id

    def disconnect(self, client_socket: socket.socket):
        client_id = self._connected_clients.pop(client_socket)
        self._available_ids.append(client_id)

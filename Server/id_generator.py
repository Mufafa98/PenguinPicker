import socket
import threading

ID_LOCK = threading.Lock()


class IdTool:
    """
    ### About
    - This class is responsible for generating unique ids for each client.
    - It also keeps track of the connected clients, and the available ids.
    ### Methods
    - connect(client_socket: socket.socket) -> int:
        - This method is called when a new client connects to the server.
        - It returns a unique id for the client.
    - disconnect(client_socket: socket.socket):
        - This method is called when a client disconnects from the server.
        - It frees up the id of the client.
    """

    def __init__(self):
        """
        ### About
        - This method initializes the class.
        ### Attributes
        - _connected_clients: dict
            - This dictionary stores the connected clients and their ids.
        - _available_ids: list
            - This list stores the ids that are available for use.
        - _counter: int
            - This variable stores the last id that was assigned to a client.
        """
        self._connected_clients = dict()
        self._available_ids = list()
        self._counter = 0

    def connect(self, client_socket: socket.socket) -> int:
        """
        ### About
        - This method is called when a new client connects to the server.
        ### Parameters
        - client_socket: socket.socket
            - This is the socket object of the client.
        ### Returns
        - int
            - This is the unique id assigned to the client.
        """
        global ID_LOCK
        with ID_LOCK:
            if self._available_ids == []:
                self._connected_clients[client_socket] = self._counter
                self._counter += 1
                return self._counter - 1
            else:
                new_id = self._available_ids.pop(0)
                self._connected_clients[client_socket] = new_id
                return new_id

    def disconnect(self, client_socket: socket.socket):
        """
        ### About
        - This method is called when a client disconnects from the server.
        - The function frees up the id of the client. for future use.
        ### Parameters
        - client_socket: socket.socket
            - This is the socket object of the client.
        """
        global ID_LOCK
        with ID_LOCK:
            client_id = self._connected_clients.pop(client_socket)
            self._available_ids.append(client_id)

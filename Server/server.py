import socket
import threading
from Utils import Message, Protocol, SERVER_PORT, SERVER_IP
from .id_generator import IdGenerator
import random
import logging

id_tool = IdGenerator()
"""Generator for clients ids"""

GAMES_LOCK = threading.Lock()
"""Lock for the games dictionary"""
GAMES = dict()
"""Games that are currently beeing played"""

CLIENT_LOCK = threading.Lock()
"""Lock for the client queue"""
CLIENT_QUEUE = dict()
"""Mapping between clients and their ids"""


MULTIPLAYER_QUEUE = list()
"""Clients that are waiting to play an online game"""
MULTIPLAYER_LOCK = threading.Lock()
"""Lock for the multiplayer queue"""


def handle_client(client_socket: socket.socket):
    """
    ### About
    Function that has to handle the connection with a client.

    ### Parameters
    client_socket: Socket object that assures the communication
    between the server and the client

    ### Exceptions
    Exception: if an error ocurs when converting from bytes to Message
    """
    global GAMES_LOCK, GAMES
    global CLIENT_LOCK, CLIENT_QUEUE
    global MULTIPLAYER_QUEUE, MULTIPLAYER_LOCK

    with client_socket:
        # Generate and send the client id
        client_id = id_tool.connect(client_socket)
        client_socket.send(
            Message(Protocol.ID, str(client_id))
            .to_bytes()
        )
        
        # Recive a confirmation message and store the client id
        client_socket.recv(1024)
        client_socket.sendall(
            Message(Protocol.PONG, "").to_bytes()
        )

        with CLIENT_LOCK:
            CLIENT_QUEUE[client_id] = client_socket
        while True:
            try:    
                message = Message.from_bytes(client_socket.recv(1024))
                if message.protocol == Protocol.EXIT:
                    logging.info(f"Client {client_id} disconnected")
                    # If a client disconects and is in the middle
                    # of a game, tell the opponent thet he won
                    with GAMES_LOCK:
                        if client_id in GAMES:
                            other_player = GAMES[client_id]
                            CLIENT_QUEUE[other_player].sendall(
                                Message(Protocol.WIN, "").to_bytes()
                            )
                            del GAMES[client_id]
                            del GAMES[other_player]
                    break
                elif message.protocol == Protocol.START:
                    # The client is ready to play and he'll be
                    # added to the waiting queue
                    if client_id not in MULTIPLAYER_QUEUE:
                        with MULTIPLAYER_LOCK:
                            MULTIPLAYER_QUEUE.append((client_id, message.data))
                    elif message.protocol == Protocol.PENGUIN:
                        message = Message(Protocol.PENGUIN, message.data)
                        CLIENT_QUEUE[GAMES[client_id]].sendall(message.to_bytes())
                    elif message.protocol == Protocol.WALL:
                        message = Message(Protocol.WALL, message.data)
                        CLIENT_QUEUE[GAMES[client_id]].sendall(message.to_bytes())
                # If there are at least two players in the queue
                # a match can be created
                with MULTIPLAYER_LOCK:
                    mp_queue_len = len(MULTIPLAYER_QUEUE)
                    if (mp_queue_len % 2 == 0 and mp_queue_len != 0):
                            # Get the first two players
                            player1 = MULTIPLAYER_QUEUE.pop(0)
                            player2 = MULTIPLAYER_QUEUE.pop(0)

                            name1 = player1[1]
                            name2 = player2[1]

                            GAMES[player1[0]] = player2[0]
                            GAMES[player2[0]] = player1[0]

                            # Generate the same board for the two players
                            # using a common seed
                            seed = random.randint(0, 1000)
                            turns = random.randint(0, 1)
                            if turns == 1:
                                name1, name2 = name2, name1
                            CLIENT_QUEUE[player1[0]].sendall(
                                Message(
                                    Protocol.START,
                                    f"{seed} {turns} {name1} {name2}"
                                ).to_bytes()
                            )
                            CLIENT_QUEUE[player2[0]].sendall(
                                Message(
                                    Protocol.START,
                                    f"{seed} {1 - turns} {name1} {name2}"
                                ).to_bytes()
                            )
            except Exception as e:
                logging.error(f"An error occurred: {e}")
                break
        # When the client disconects, remove it's id from memmory
        id_tool.disconnect(client_socket)

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def run():
    """
    ### About
    Function responsable for starting a server and managing it's connections
    ### Exceptions
    KeyboardInterrupt in order to force stop the server if needed
    """
    setup_logging()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((SERVER_IP, SERVER_PORT))
    server.listen()
    logging.info(f"Server listening on port {SERVER_PORT}")

    threads = []
    stop_event = threading.Event()

    def accept_clients():
        """
        ### About
        This function accepts a client and creates a separate thread
        responsable for managing it's requests
        """
        while not stop_event.is_set():
            try:
                server.settimeout(1.0)
                client_socket, addr = server.accept()
                logging.info(
                    f"Accepted connection from {addr}"
                )
                client_handler = threading.Thread(
                    target=handle_client,
                    args=(client_socket,)
                )
                client_handler.start()
                threads.append(client_handler)
            except socket.timeout:
                continue

    accept_thread = threading.Thread(target=accept_clients)
    accept_thread.start()

    try:
        accept_thread.join()
    except KeyboardInterrupt:
        logging.info("Shutting down server...")
        stop_event.set()
        accept_thread.join()
    finally:
        for thread in threads:
            thread.join()
        server.close()
        for sock in CLIENT_QUEUE.values():
            sock.close()
        CLIENT_QUEUE.clear()

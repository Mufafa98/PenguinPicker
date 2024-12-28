import socket
import threading
from colortag import cprint
from Utils import Message, Protocol, SERVER_PORT, SERVER_IP
from .id_generator import IdTool
import random

id_tool = IdTool()

GAMES_LOCK = threading.Lock()
GAMES = dict()

CLIENT_LOCK = threading.Lock()
CLIENT_QUEUE = dict()

MULTIPLAYER_QUEUE = list()
MULTIPLAYER_LOCK = threading.Lock()


def handle_client(client_socket: socket.socket):
    global GAMES_LOCK
    global GAMES
    global CLIENT_LOCK
    global CLIENT_QUEUE
    global MULTIPLAYER_QUEUE
    global MULTIPLAYER_LOCK

    with client_socket:
        # Generate and send the client id
        client_id = id_tool.connect(client_socket)
        message = Message(Protocol.ID, str(client_id))
        client_socket.send(message.to_bytes())
        # Recive a random message
        request = client_socket.recv(1024)
        cprint(f"Received: {request.decode('utf-8')}")
        message = Message(Protocol.PONG, "Hello, Client!")
        client_socket.sendall(message.to_bytes())
        cprint("[<Success: green;bold>]: Connection established")
        with CLIENT_LOCK:
            CLIENT_QUEUE[client_id] = client_socket
        while True:
            try:
                data = client_socket.recv(1024)
                message = Message.from_bytes(data)
                if message.protocol == Protocol.EXIT:
                    cprint(f"Client {client_id} disconnected")
                    if client_id in GAMES:
                        with GAMES_LOCK:
                            other_player = GAMES[client_id]
                            CLIENT_QUEUE[other_player].sendall(
                                Message(Protocol.WIN, "").to_bytes()
                            )
                            del GAMES[client_id]
                            del GAMES[other_player]
                    break
                elif message.protocol == Protocol.START:
                    cprint(f"Client {client_id} is ready to play")
                    if client_id not in MULTIPLAYER_QUEUE:
                        cprint(f"Adding {client_id} to the multiplayer queue")
                        with MULTIPLAYER_LOCK:
                            MULTIPLAYER_QUEUE.append((client_id, message.data))
                elif message.protocol == Protocol.PENGUIN:
                    message = Message(Protocol.PENGUIN, message.data)
                    CLIENT_QUEUE[GAMES[client_id]].sendall(message.to_bytes())
                elif message.protocol == Protocol.WALL:
                    message = Message(Protocol.WALL, message.data)
                    CLIENT_QUEUE[GAMES[client_id]].sendall(message.to_bytes())
                if (len(MULTIPLAYER_QUEUE) % 2 == 0 and
                    len(MULTIPLAYER_QUEUE) != 0
                    ):
                    cprint("[<Success: green;bold>]: Starting game...")
                    with MULTIPLAYER_LOCK:
                        player1 = MULTIPLAYER_QUEUE.pop(0)
                        player2 = MULTIPLAYER_QUEUE.pop(0)
                        cprint(f"Player 1: {player1}")
                        cprint(f"Player 2: {player2}")
                        GAMES[player1[0]] = player2[0]
                        GAMES[player2[0]] = player1[0]
                        random_seed = random.randint(0, 1000)
                        turns = random.randint(0, 1)
                        name1 = player1[1]
                        name2 = player2[1]
                        if turns == 1:
                            name1, name2 = name2, name1
                        send = f"{random_seed} {turns} {name1} {name2}"
                        CLIENT_QUEUE[player1[0]].sendall(
                            Message(
                                Protocol.START,
                                send).to_bytes()
                        )
                        send = f"{random_seed} {1 - turns} {name1} {name2}"
                        CLIENT_QUEUE[player2[0]].sendall(
                            Message(
                                Protocol.START,
                                send).to_bytes()
                        )

            except Exception as e:
                cprint(f"An error occurred: {e}")
                break
        id_tool.disconnect(client_socket)


def run():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((SERVER_IP, SERVER_PORT))
    server.listen()
    cprint(f"[<Success: green;bold>]: Server listening on port {SERVER_PORT}")

    threads = []
    stop_event = threading.Event()

    def accept_clients():
        while not stop_event.is_set():
            try:
                server.settimeout(1.0)
                client_socket, addr = server.accept()
                cprint(
                    f"[<Success: green;bold>]: Accepted connection from {addr}"
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
        while True:
            pass
    except KeyboardInterrupt:
        cprint("[< Info  : gray;bold>]: Shutting down server...")
        stop_event.set()
        accept_thread.join()
    finally:
        for thread in threads:
            thread.join()
        server.close()

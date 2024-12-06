import socket
import threading
from colortag import cprint
from Utils import Message, Protocol, SERVER_PORT, SERVER_IP
from .id_generator import IdTool

id_tool = IdTool()


def handle_client(client_socket: socket.socket):
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
        id_tool.disconnect(client_socket)


def run():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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

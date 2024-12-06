import socket
from colortag import cprint
from Utils import Message, Protocol, SERVER_IP, SERVER_PORT


def run():
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Connect to the server
        client_socket.connect((SERVER_IP, SERVER_PORT))
        cprint(
            f"[<Success: green;bold>]: Connected to {SERVER_IP}:{SERVER_PORT}"
            )
        # Recive some data
        message = client_socket.recv(1024)
        decoded_message = Message.from_bytes(message)
        print(f"Recived id {decoded_message} from server")
        # Send some data
        message = Message(Protocol.PING, "Hello, Server!")
        client_socket.sendall(message.to_bytes())
        # Receive data from the server
        response = client_socket.recv(1024)
        message = Message.from_bytes(response).data
        cprint(f"Received from server: {message}")
        while True:
            pass
    except KeyboardInterrupt:
        cprint("Shutting down client...")
    except Exception as e:
        cprint(f"An error occurred: {e}")
    finally:
        # Close the connection
        client_socket.close()
        cprint("[<Success: green;bold>]: Connection closed")

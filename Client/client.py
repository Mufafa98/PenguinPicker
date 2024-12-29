import socket
from colortag import cprint
from Utils import Message, Protocol, SERVER_IP, SERVER_PORT

from .gui import start_gui


def run():
    """
    ### About
    - This function is the entry point for the client.
    - It connects to the server and starts the GUI.
    ### Exceptions
    - KeyboardInterrupt: If the user presses `Ctrl+C`, the client will shut down.
    - Exception: If an error occurs, the client will print the error.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Connects to the server and recive its id
        client_socket.connect((SERVER_IP, SERVER_PORT))
        cprint(
            f"[<Success: green;bold>]: Connected to {SERVER_IP}:{SERVER_PORT}"
        )
        message = client_socket.recv(1024)
        decoded_message = Message.from_bytes(message)
        print(f"Recived id {decoded_message} from server")
        # Send a confirmation message
        message = Message(Protocol.PING, "Hello, Server!")
        client_socket.sendall(message.to_bytes())
        # Receive data from the server
        response = client_socket.recv(1024)
        message = Message.from_bytes(response).data
        cprint(f"Received from server: {message}")
        start_gui(client_socket)
    except KeyboardInterrupt:
        cprint("Shutting down client...")
    except Exception as e:
        cprint(f"An error occurred: {e}")
    finally:
        # Close the connection
        client_socket.close()
        cprint("[<Success: green;bold>]: Connection closed")

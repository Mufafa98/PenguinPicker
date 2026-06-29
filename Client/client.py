import logging
import socket
from Utils import Message, Protocol, SERVER_IP, SERVER_PORT

import os
import warnings

# Hide "Hello from the pygame community" and AVX2 TuntimeWarning
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
warnings.filterwarnings("ignore", message=".*avx2 capable.*")

from Client.gui import start_gui

def run():
    """
    ### About
    - This function is the entry point for the client.
    - It connects to the server and starts the GUI.
    ### Exceptions
    - KeyboardInterrupt: If the user presses `Ctrl+C`, the client
    will shut down.
    - Exception: If an error occurs, the client will print the error.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Connects to the server and recive its id
        client_socket.connect((SERVER_IP, SERVER_PORT))
        logging.info(f"Connected to {SERVER_IP}:{SERVER_PORT}")

        client_socket.recv(1024)
        # Send a confirmation message
        message = Message(Protocol.PING, "")
        client_socket.sendall(message.to_bytes())
        # Receive data from the server
        response = client_socket.recv(1024)
        message = Message.from_bytes(response).data
        logging.info(f"Received from server: {message}")
        start_gui(client_socket)
    except KeyboardInterrupt:
        logging.info("Shutting down client...")
    except Exception as e:
        logging.info(f"An error occurred: {e}")
    finally:
        # Close the connection
        client_socket.close()
        logging.info("Connection closed")

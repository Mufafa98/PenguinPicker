import pygame
import sys
import socket
from .penguin_engine import Engine
from .menu import Menu
from .gui_params import FPS, BACKGROUND_COLOR, game_state, SCREEN_SIZE
from .click_dispatcher import ClickDispatcher
from Utils.protocol import Protocol, Message


def start_gui(client_socket: socket.socket):
    """
    ### About
    - This function is the entry point for the GUI.
    - It initializes the pygame engine and starts the game loop.
    ### Parameters
    - `client_socket`: The socket object used to communicate with the server.
    """
    global game_state, assets, SCREEN_SIZE, BACKGROUND_COLOR, FPS

    # Initialize a dispatcher to handle clicks
    dispatcher = ClickDispatcher()

    # Create a interface for the game and register its objects
    # with the dispatcher
    menu = Menu(client_socket)
    dispatcher.register_objects(menu.used_ids(), menu)
    engine = None

    pygame.init()

    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Penguin Picker")

    # Set up a clock responsable for the FPS
    clock = pygame.time.Clock()

    running = True
    while running:
        # Handle `clicks`, `keys` and `exit` events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                dispatcher.dispatch_click(x, y)
            if event.type == pygame.KEYDOWN and not game_state.running:
                key = event.key
                menu.handle_key(key)
        # When tranzitioning from menu to game or game to menu
        # we need to reset the engine respectively the menu
        # in order to avoid any ghost clicks trough the dispatcher
        if game_state.engine_reset:
            print("Resetting engine")
            dispatcher.restart()
            engine = Engine(
                game_state.game_type,
                game_state.seed,
                client_socket=client_socket,
                allow_only=game_state.game_turn,
                player_1=game_state.player_1,
                player_2=game_state.player_2
            )
            dispatcher.register_objects(engine.used_ids(), engine)
            game_state.engine_reset = False
        if game_state.menu_reset:
            print("Resetting menu")
            dispatcher.restart()
            menu = Menu(client_socket)
            dispatcher.register_objects(menu.used_ids(), menu)
            game_state.menu_reset = False

        screen.fill(BACKGROUND_COLOR)

        if game_state.running:
            engine.draw(screen)
        else:
            menu.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    # When the client is done running,
    # notify the server and close the connection
    client_socket.sendall(Message(Protocol.EXIT, "").to_bytes())
    pygame.quit()
    sys.exit()

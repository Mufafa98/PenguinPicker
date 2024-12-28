import pygame
import sys
import socket
from .penguin_engine import *
from .menu import *
from .gui_params import *
from .click_dispatcher import ClickDispatcher

def start_gui(client_socket: socket.socket):
    global game_state, assests

    dispatcher = ClickDispatcher()

    menu = Menu(client_socket)
    dispatcher.register_objects(menu.used_ids(), menu)
    engine = None

    pygame.init()


    # Initialize screen
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Penguin Picker")

    # Clock for controlling frame rate
    clock = pygame.time.Clock()

    # game_state.engine_reset = True
    # game_state.game_type = 0
    # game_state.seed = 0
    # game_state.running = True

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                dispatcher.dispatch_click(x, y)
            if event.type == pygame.KEYDOWN and not game_state.running:
                key = event.key
                menu.handle_key(key)

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

        # Clear screen
        screen.fill(BACKGROUND_COLOR)

        if game_state.running:
            engine.draw(screen)
        else:
            menu.draw(screen)
        
        # Update display
        pygame.display.flip()
        clock.tick(FPS)

    client_socket.sendall(Message(Protocol.EXIT, "").to_bytes())
    pygame.quit()
    sys.exit()
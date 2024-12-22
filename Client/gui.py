import pygame
import sys
from .penguin_engine import *
from .menu import *
from .gui_params import *
from .click_dispatcher import ClickDispatcher

def start_gui():
    
    dispatcher = ClickDispatcher()

    menu = Menu()
    dispatcher.register_objects(menu.used_ids(), menu)
    # engine = Engine()
    # dispatcher.register_objects(engine.used_ids(), engine)
    


    pygame.init()

    # Initialize screen
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Penguin Picker")

    # Clock for controlling frame rate
    clock = pygame.time.Clock()

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                dispatcher.dispatch_click(x, y)
            if event.type == pygame.KEYDOWN:
                key = event.key
                menu.handle_key(key)

        # Clear screen
        screen.fill(BACKGROUND_COLOR)

        # engine.draw(screen)
        menu.draw(screen)

        # # Draw grid
        # for x in range(0, SCREEN_SIZE[0], 50):
        #     pygame.draw.line(screen, (255, 0, 0), (x, 0), (x, SCREEN_SIZE[1]))
        # for y in range(0, SCREEN_SIZE[1], 50):
        #     pygame.draw.line(screen, (255, 0, 0), (0, y), (SCREEN_SIZE[0], y))
        
        # Update display
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()
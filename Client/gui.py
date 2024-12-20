import pygame
import sys
from .penguin_engine import *
from .gui_params import *
from .click_dispatcher import ClickDispatcher

def start_gui():
    
    pygame.init()

    # Initialize screen
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Penguin Picker")

    # Clock for controlling frame rate
    clock = pygame.time.Clock()
    dispatcher = ClickDispatcher()
    engine = Engine()
    dispatcher.register_objects(engine.used_ids(), engine)

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                dispatcher.dispatch_click(x, y)

        # Clear screen
        screen.fill(BACKGROUND_COLOR)

        engine.draw(screen)

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
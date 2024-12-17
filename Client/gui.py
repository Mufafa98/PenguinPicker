import pygame
import sys


from .penguin_engine import *
import random

BACKGROUND_COLOR = (123, 123, 123)
SCREEN_SIZE = (1000, 800)
FPS = 60

def start_gui():
    
    pygame.init()

    # Initialize screen
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Penguin Picker")

    # Clock for controlling frame rate
    clock = pygame.time.Clock()

    engine = Engine()

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                print(f"Mouse clicked at ({x}, {y})")

        # Clear screen
        screen.fill(BACKGROUND_COLOR)

        engine.draw(screen)
        
        # Update display
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()
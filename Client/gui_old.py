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

    # Rectangle properties
    rect_width = 150
    rect_height = 150
    # Load texture
    textures = list()

    temp_texture = pygame.image.load('./assests/32x32/ice/ice_1_1.png')
    temp_texture = pygame.transform.scale(temp_texture, (rect_width, rect_height))
    textures.append(temp_texture)
    temp_texture = pygame.image.load('./assests/32x32/ice/ice_2_1.png')
    temp_texture = pygame.transform.scale(temp_texture, (rect_width, rect_height))
    textures.append(temp_texture)

    board = create_board()

    for line_id, line in enumerate(board):
        for column_id, column in enumerate(line):
            if column == 1:
                board[line_id][column_id] = random.randint(0, len(textures) - 1)
            elif column == 0:
                board[line_id][column_id] = -1
    # print(board)
    # Create a transparent surface
    transparent_surface = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
    transparent_surface.fill((0, 0, 0, 0))
    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                # print(f"Mouse clicked at ({x}, {y})")
                for line_id, line in enumerate(board):
                    for column_id, column in enumerate(line):
                        if column != -1:
                            hex_x = column_id * 0.5 * rect_width
                            hex_y = line_id * 0.75 * rect_height
                            hex_rect = pygame.Rect(hex_x, hex_y, rect_width, rect_height)
                            if hex_rect.collidepoint(x, y):
                                print(f"Clicked on hexagon at ({line_id}, {column_id})")
                                # Perform any additional actions here

        # Clear screen
        screen.fill(BACKGROUND_COLOR)

        for line_id, line in enumerate(board):
            for column_id, column in enumerate(line):
                if column != -1:
                    screen.blit(
                        transparent_surface, 
                        (column_id * 0.5 * rect_width, line_id * 0.75 * rect_height)
                        )
                    screen.blit(
                        textures[column], 
                        (column_id * 0.5 * rect_width, line_id * 0.75 * rect_height))

        # Update display
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()
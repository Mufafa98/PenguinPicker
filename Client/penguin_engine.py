import pygame
import enum
import math
import sys

class Tile(enum.Enum):
    EMPTY = 0
    ICE = 1

HEX_COORDS_COEF = [
    (0.0, -1.0),
    (1.0, -0.5),
    (1.0, 0.5),
    (0.0, 1.0),
    (-1.0, 0.5),
    (-1.0, -0.5),
]

DEFAULT_BOARD = [
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0 ,1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1 ,0],
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0 ,1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1 ,0],
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0 ,1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1 ,0],
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0 ,1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1 ,0],
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0 ,1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1 ,0],
]

def create_board() -> list:
    board = []
    for line in DEFAULT_BOARD:
        temp_line = []
        for cell in line:
            if cell == 0:
                temp_line.append(Tile.EMPTY)
            else:
                temp_line.append(Tile.ICE)
        board.append(temp_line)
    return board

class Engine:
    def __init__(self, board: list = None, hex_size: int = 50, platform_start: tuple = (0, 0)):
        if board is None:
            board = create_board()
        self.board = board
        self.hex_size = hex_size
        self.platform_start = platform_start
        self.hex_coords = dict()
        for y, row in enumerate(board):
            for x, tile in enumerate(row):
                if tile == Tile.ICE:
                    self.hex_coords[(x, y)] = self.hexagon(
                        x,
                        y * 1.5
                        )
    

    def hexagon(self, x: int, y: int) -> list:
        x_offset = self.platform_start[0] + (x + 1) * self.hex_size 
        y_offset = self.platform_start[1] + (y + 1) * self.hex_size 

        return [
            [x_offset + self.hex_size * coef[0], y_offset + self.hex_size * coef[1]] 
            for coef in HEX_COORDS_COEF
        ]


    def draw(self, screen: pygame.Surface):
        counter = 0x000000
        for hex_coords in self.hex_coords.values():
            pygame.draw.polygon(screen, counter, hex_coords)
            counter += 0x00010
        # sys.exit()
        

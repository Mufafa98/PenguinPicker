import pygame
import enum
import sys
import time

from ..gui_params import *

class Tile(enum.Enum):
    EMPTY = 0
    ICE = 1

HEX_COORDS_COEF_OLD = [
    (0.0, -1.0),
    (1.0, -0.5),
    (1.0, 0.5),
    (0.0, 1.0),
    (-1.0, 0.5),
    (-1.0, -0.5),
]
HEX_COORDS_COEF = [
    (0.5, 0.0),
    (1, 0.25),
    (1, 0.75),
    (0.5, 1),
    (0, 0.75),
    (0, 0.25),
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

DEFAULT_BOARD_V2 = [
    [0, 1, 0, 1, 0, 1, 0],
    [1, 0, 1, 0, 1, 0, 1],
    [0, 1, 0, 1, 0, 1, 0],
    [1, 0, 1, 0, 1, 0, 1],
]

OBJECT_ID = 0

def create_board() -> list:
    board = []
    for line in DEFAULT_BOARD_V2:
        temp_line = []
        for cell in line:
            if cell == 0:
                temp_line.append(Tile.EMPTY)
            else:
                temp_line.append(Tile.ICE)
        board.append(temp_line)
    return board

class Hexagon:
    def __init__(self, x: int, y: int, size: int, obj_id: int, color: int = 0x000000):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.obj_id = obj_id
        self.points = [
            [
                x + self.size * coef[0], 
                y + self.size * coef[1]
            ] for coef in HEX_COORDS_COEF
        ]
        # print(self.points)
        x_start = int(x)
        y_start = int(y - size)
        x_end = int(x_start + size)
        y_end = int(y_start + size)
        for temp_x in range(x_start, x_end):
            for temp_y in range(y_start, y_end):
                if self.point_in_hexagon(temp_x, temp_y):
                    index_buffer[temp_y][temp_x] = (self.obj_id)

    def point_in_hexagon(self, x: int, y: int) -> bool:
        if y < self.points[1][1] or y > self.points[2][1]:
            return True
        return True


class Engine:
    def __init__(self, board: list = None, hex_size: int = 50, platform_start: tuple = (0, 0)):
        global OBJECT_ID
        if board is None:
            board = create_board()
        self.board = board
        self.hex_size = hex_size
        self.platform_start = platform_start
        self.hex_objects = dict()
        counter = 0x000000
        for y, row in enumerate(board):
            for x, tile in enumerate(row):
                if tile == Tile.ICE:
                    self.hex_objects[OBJECT_ID] = Hexagon(
                        platform_start[0] + (x) * hex_size, 
                        platform_start[1] + (y * 1.5) * hex_size, 
                        hex_size, OBJECT_ID, counter)
                    counter += 0x203010
                    OBJECT_ID += 1


    def draw(self, screen: pygame.Surface):
        for hexagon in self.hex_objects.values():
            pygame.draw.polygon(screen, hexagon.color, hexagon.points)
        # sys.exit()
        

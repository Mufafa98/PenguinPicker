import pygame
import enum
import sys
import time

from .gui_params import *

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
        x_start = int(x)
        y_start = int(y)
        x_end = int(x_start + size)
        y_end = int(y_start + size)
        for temp_y in range(y_start, y_end):
            for temp_x in range(x_start, x_end):
                if self.point_in_hexagon(temp_x, temp_y):
                    index_buffer[temp_y][temp_x] = (self.obj_id)

    def point_in_hexagon(self, x: int, y: int) -> bool:
        def triangle_area(A: tuple, B: tuple, C: tuple):
            return abs((A[0]*(B[1]-C[1]) + B[0]*(C[1]-A[1]) + C[0]*(A[1]-B[1]))/2.0)
        if y <= self.points[1][1]:
            a, b, c = self.points[0], self.points[1], self.points[5]
            main_area = triangle_area(a, b, c)
            area1 = triangle_area((x, y), a, b)
            area2 = triangle_area((x, y), b, c)
            area3 = triangle_area((x, y), c, a)
            return main_area == area1 + area2 + area3
        elif y >= self.points[2][1]:
            a, b, c = self.points[2], self.points[3], self.points[4]
            main_area = triangle_area(a, b, c)
            area1 = triangle_area((x, y), a, b)
            area2 = triangle_area((x, y), b, c)
            area3 = triangle_area((x, y), c, a)
            return main_area == area1 + area2 + area3
        return True

class Engine(Supervisor):
    def __init__(self, board: list = None, hex_size: int = 100, platform_start: tuple = (0, 0)):
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
                        platform_start[0] + (x * 0.5) * hex_size, 
                        platform_start[1] + (y * 0.75) * hex_size, 
                        hex_size, OBJECT_ID, counter)
                    counter += 0x203010
                    OBJECT_ID += 1

    def handle_click(self, x: int, y: int, obj_id: int):
        self.hex_objects[obj_id].color += 0x00F000

    def used_ids(self) -> list:
        return list(self.hex_objects.keys())

    def draw(self, screen: pygame.Surface):
        for hexagon in self.hex_objects.values():
            pygame.draw.polygon(screen, hexagon.color, hexagon.points)
        

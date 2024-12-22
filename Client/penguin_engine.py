import pygame
import random
import enum
import sys
import time

from .gui_params import *
import os

class Tile:
    EMPTY               = 0b0000000
    PENGUIN             = 0b0000001
    ICE                 = 0b0000010
    CRACKED_ICE         = 0b0000100
    FINISH              = 0b0001000

class Turn:
    PENGUIN = 0b0
    WALL = 0b1

class GameStatus:
    RUNNING = 0b0
    PENGUIN_WON = 0b1
    CRACKER_WON = 0b10

HEX_COORDS_COEF = [
    (0.5, 0.0),
    (1, 0.25),
    (1, 0.75),
    (0.5, 1),
    (0, 0.75),
    (0, 0.25),
]


def create_board(lines: int, cols: int, crack_percent: float, penguin_pos: tuple = None) -> list:
    board = []
    for line in range(lines):
        temp_line = []
        for col in range(cols * 2 - 1):
            if (line + col) % 2 == 1:
                if line == 0 or line == lines - 1 or col <= 1 or col >= cols * 2 - 3:
                    temp_line.append(Tile.FINISH | Tile.ICE)
                else:
                    if random.random() < crack_percent:
                        temp_line.append(Tile.CRACKED_ICE)
                    else:
                        temp_line.append(Tile.ICE)
            else:
                temp_line.append(Tile.EMPTY)
        board.append(temp_line)
    if penguin_pos is None:
        mid_pos = (len(board[0]) // 2, len(board) // 2)
        if board[mid_pos[1]][mid_pos[0]] == Tile.EMPTY:
            mid_pos = (mid_pos[0] - 1, mid_pos[1])
        board[mid_pos[1]][mid_pos[0]] = Tile.ICE | Tile.PENGUIN
    else:
        board[penguin_pos[1]][penguin_pos[0]] = Tile.ICE | Tile.PENGUIN
    return board

class Hexagon:
    def __init__(self, platform_start: tuple, x: int, y: int, size: int, obj_id: int, color: int = 0x000000):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.obj_id = obj_id
        screen_x = platform_start[0] + (x * 0.5) * size
        screen_y = platform_start[1] + (y * 0.75) * size
        self.points = [
            [
                screen_x + self.size * coef[0], 
                screen_y + self.size * coef[1]
            ] for coef in HEX_COORDS_COEF
        ]
        x_start = int(screen_x)
        y_start = int(screen_y)
        x_end = int(x_start + size)
        y_end = int(y_start + size)
        for temp_y in range(y_start, y_end):
            for temp_x in range(x_start, x_end):
                if self.point_in_hexagon(temp_x, temp_y):
                    if temp_x < 0 or temp_x >= SCREEN_SIZE[0] or temp_y < 0 or temp_y >= SCREEN_SIZE[1]:
                        continue
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

    def clone(self):
        return Hexagon(self.x, self.y, self.size, self.obj_id, self.color)

    def __str__(self):
        return f"Hexagon({self.x}, {self.y}, {self.size}, {self.obj_id})\n"
    def __repr__(self):
        return self.__str__()

def center_board(board_size: tuple, hex_size: int) -> tuple:
    board_width = board_size[0] * hex_size
    board_height = (((board_size[1] + 1 )/ 2) * hex_size + 
                    board_size[1] / 2 * hex_size / 2)
    return ((SCREEN_SIZE[0] - board_width) / 2, 
            (SCREEN_SIZE[1] - board_height) / 2)
def snow_texture(board: list, x: int, y: int) -> pygame.Surface:
        global TEXTURES
        def get_board_tile(board: list, x: int, y: int) -> int:
            try:
                if board[y][x] & Tile.FINISH != 0:
                    return Tile.EMPTY
                elif board[y][x] & Tile.CRACKED_ICE != 0:
                    return Tile.ICE
                elif board[y][x] & Tile.ICE != 0:
                    return Tile.ICE
                return board[y][x]
            except IndexError:
                return Tile.EMPTY
        neighbors = [
            get_board_tile(board, x - 1, y - 1),
            get_board_tile(board, x + 1, y - 1),
            get_board_tile(board, x + 2, y),
            get_board_tile(board, x + 1, y + 1),
            get_board_tile(board, x - 1, y + 1),
            get_board_tile(board, x - 2, y),
        ]
        if neighbors[0] == Tile.ICE and neighbors[1] == Tile.ICE:
            return TEXTURES['SNOW_BOTTOM']
        elif neighbors[0] == Tile.ICE and neighbors[4] == Tile.ICE:
            return TEXTURES['SNOW_LEFT']
        elif neighbors[5] == Tile.ICE:
            return TEXTURES['SNOW_SLEFT']
        elif neighbors[0] == Tile.ICE:
            return TEXTURES['SNOW_BLEFT']
        elif neighbors[1] == Tile.ICE and neighbors[3] == Tile.ICE:
            return TEXTURES['SNOW_RIGHT']
        elif neighbors[2] == Tile.ICE:
            return TEXTURES['SNOW_SRIGHT']
        elif neighbors[1] == Tile.ICE:
            return TEXTURES['SNOW_BRIGHT']
        elif neighbors[3] == Tile.ICE and neighbors[4] == Tile.ICE:
            return TEXTURES['SNOW_TOP']
        elif neighbors[3] == Tile.ICE:
            return TEXTURES['SNOW_TRIGHT']
        elif neighbors[4] == Tile.ICE:
            return TEXTURES['SNOW_TLEFT']
        return None



class Engine(Supervisor):
    def __init__(self, board_size: tuple = (16, 15), hex_size: int = 64):
        global OBJECT_ID
        self.board = create_board(board_size[1], board_size[0], 0.2)
        self.hex_size = hex_size
        # board_width = board_size[0] * hex_size
        # board_height = (((board_size[1] + 1 )/ 2) * hex_size + 
        #                 board_size[1] / 2 * hex_size / 2)
        # self.platform_start = ((SCREEN_SIZE[0] - board_width) / 2, 
        #                        (SCREEN_SIZE[1] - board_height) / 2)
        self.platform_start = center_board(board_size, hex_size)
        self.hex_objects = dict()
        for y, row in enumerate(self.board):
            for x, tile in enumerate(row):
                if tile & Tile.ICE != 0 or tile & Tile.CRACKED_ICE != 0:
                    if tile & Tile.PENGUIN != 0:
                        self.penguin_pos = (x, y)
                        self.penguin_id = OBJECT_ID
                    self.hex_objects[OBJECT_ID] = Hexagon(
                        self.platform_start, x, y, 
                        hex_size, OBJECT_ID)
                    OBJECT_ID += 1
        self.turn = Turn.PENGUIN
        self.game_status = GameStatus.RUNNING
                    

    def handle_click(self, x: int, y: int, obj_id: int):
        if obj_id in self.hex_objects and self.game_status == GameStatus.RUNNING:
            if self.turn == Turn.PENGUIN:
                self.move_penguin(x, y, obj_id)
            elif self.turn == Turn.WALL:
                self.place_wall(x, y, obj_id)
        else:
            print(f"Invalid click: Game Finished: {self.game_status}")

    def legal_for_penguin(self) -> bool:
        def inside_board(x: int, y: int) -> bool:
            return 0 <= x < len(self.board[0]) and 0 <= y < len(self.board)
        penguin_obj = self.hex_objects[self.penguin_id]
        return (
            (inside_board(penguin_obj.x - 2, penguin_obj.y) and 
             self.board[penguin_obj.y][penguin_obj.x - 2] & Tile.ICE != 0)
             or (inside_board(penguin_obj.x + 2, penguin_obj.y) and
                 self.board[penguin_obj.y][penguin_obj.x + 2] & Tile.ICE != 0)
             or (inside_board(penguin_obj.x - 1, penguin_obj.y - 1) and
                 self.board[penguin_obj.y - 1][penguin_obj.x - 1] & Tile.ICE != 0)
             or (inside_board(penguin_obj.x + 1, penguin_obj.y - 1) and
                 self.board[penguin_obj.y - 1][penguin_obj.x + 1] & Tile.ICE != 0)
             or (inside_board(penguin_obj.x - 1, penguin_obj.y + 1) and
                 self.board[penguin_obj.y + 1][penguin_obj.x - 1] & Tile.ICE != 0)
             or (inside_board(penguin_obj.x + 1, penguin_obj.y + 1) and
                 self.board[penguin_obj.y + 1][penguin_obj.x + 1] & Tile.ICE != 0)
        )

    def move_penguin(self, x: int, y: int, obj_id: int):
        penguin_obj = self.hex_objects[self.penguin_id]
        current_obj = self.hex_objects[obj_id]
        if self.board[current_obj.y][current_obj.x] & Tile.ICE == 0:
            return
        if abs(penguin_obj.x - current_obj.x) > 2 or abs(penguin_obj.y - current_obj.y) > 1:
            return
        penguin_obj.color, current_obj.color = current_obj.color, penguin_obj.color
        self.board[penguin_obj.y][penguin_obj.x] = Tile.ICE
        self.penguin_id = obj_id
        self.board[current_obj.y][current_obj.x] = Tile.PENGUIN | self.board[current_obj.y][current_obj.x]
        self.turn = Turn.WALL
        if self.board[current_obj.y][current_obj.x] & Tile.FINISH != 0:
            self.game_status = GameStatus.PENGUIN_WON
    
    def place_wall(self, x: int, y: int, obj_id: int):
        current_obj = self.hex_objects[obj_id]
        if (self.board[current_obj.y][current_obj.x] & Tile.PENGUIN != 0 or 
            self.board[current_obj.y][current_obj.x] & Tile.FINISH != 0):
            return
        self.board[current_obj.y][current_obj.x] = Tile.CRACKED_ICE
        self.hex_objects[obj_id].color = 0xA0A0A0
        self.turn = Turn.PENGUIN
        if not self.legal_for_penguin():
            self.game_status = GameStatus.CRACKER_WON

    def used_ids(self) -> list:
        return list(self.hex_objects.keys())

    
    def penguin_texture(self) -> pygame.Surface:
        if self.game_status == GameStatus.PENGUIN_WON:
            return self.textures['PENGUIN']
        elif self.legal_for_penguin():
            return self.textures['PENGUIN_SCARED']
        return self.textures['PENGUIN_SAD']

    def draw(self, screen: pygame.Surface):
        for hexagon in self.hex_objects.values():
            if self.board[hexagon.y][hexagon.x] & Tile.CRACKED_ICE != 0:
                top_left_neigh = self.board[hexagon.y - 1][hexagon.x - 1]
                top_left_neigh = top_left_neigh & Tile.ICE 
                top_right_neigh = self.board[hexagon.y - 1][hexagon.x + 1]
                top_right_neigh = top_right_neigh & Tile.ICE 
                if top_left_neigh and top_right_neigh:
                    screen.blit(self.textures['HOLE_HALF'], (hexagon.points[0][0] - self.hex_size / 2, hexagon.points[0][1]))
                elif top_left_neigh:
                    screen.blit(self.textures['HOLE_HALF_LEFT'], (hexagon.points[0][0] - self.hex_size / 2, hexagon.points[0][1]))
                elif top_right_neigh:
                    screen.blit(self.textures['HOLE_HALF_RIGHT'], (hexagon.points[0][0] - self.hex_size / 2, hexagon.points[0][1]))
                else:
                    screen.blit(self.textures['HOLE_FULL'], (hexagon.points[0][0] - self.hex_size / 2, hexagon.points[0][1]))
            elif (self.board[hexagon.y][hexagon.x] & Tile.ICE != 0 and 
                  self.board[hexagon.y][hexagon.x] & Tile.FINISH == 0):
                screen.blit(self.textures['ICE_BORDER'], (hexagon.points[0][0] - self.hex_size / 2, hexagon.points[0][1]))
            elif self.board[hexagon.y][hexagon.x] & Tile.FINISH != 0:
                texture = snow_texture(self.board, hexagon.x, hexagon.y)
                if texture is not None:
                    screen.blit(texture, (hexagon.points[0][0] - self.hex_size / 2, hexagon.points[0][1]))  
            if hexagon.obj_id == self.penguin_id:
                screen.blit(self.penguin_texture(), (hexagon.points[0][0] - self.hex_size / 2, hexagon.points[0][1] - self.hex_size * 0.25))

        font = pygame.font.Font(None, 36)
        if self.game_status & GameStatus.PENGUIN_WON != 0:
            text = font.render("PENGUIN WON", True, (255, 255, 255))
            screen.blit(text, (0, 0))
        elif self.game_status & GameStatus.CRACKER_WON != 0:
            text = font.render("CRACKER WON", True, (255, 255, 255))
            screen.blit(text, (0, 0))
        

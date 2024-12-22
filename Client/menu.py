from .gui_params import *
from .penguin_engine import Hexagon, create_board, Tile, center_board, snow_texture

import pygame

class Username:
    def __init__(self):
        global OBJECT_ID
        global TILE_SIZE
        self.username = ""
        self.penguin_pos = (2, 1)
        self.board = create_board(3, 16, 0, self.penguin_pos)
        self.objects = dict()
        start_pos = (center_board((16, 3), TILE_SIZE)[0], 0)
        for y, row in enumerate(self.board):
            for x, tile in enumerate(row):
                self.objects[OBJECT_ID] = Hexagon(
                    start_pos, x, y, 
                    TILE_SIZE, OBJECT_ID)
                OBJECT_ID += 1
    
    def pop(self):
        self.username = self.username[:-1]
        if self.penguin_pos[0] - 2 < 1:
            return
        self.board[self.penguin_pos[1]][self.penguin_pos[0]] = Tile.ICE
        self.board[self.penguin_pos[1]][self.penguin_pos[0] - 2] =Tile.ICE | Tile.PENGUIN
        self.penguin_pos = (self.penguin_pos[0] - 2, self.penguin_pos[1])
    
    def push(self, char):
        if self.penguin_pos[0] + 2 >= len(self.board[0]) - 1:
            return
        self.username += char
        self.board[self.penguin_pos[1]][self.penguin_pos[0]] = Tile.CRACKED_ICE
        self.board[self.penguin_pos[1]][self.penguin_pos[0] + 2] |= Tile.PENGUIN
        self.penguin_pos = (self.penguin_pos[0] + 2, self.penguin_pos[1])

    def draw(self, screen: pygame.Surface):
        for obj in self.objects.values():
            # pygame.draw.polygon(screen, obj.color, obj.points)
            if type(obj) == Hexagon:
                if self.board[obj.y][obj.x] & Tile.FINISH != 0:
                    texture = snow_texture(self.board, obj.x, obj.y)
                    if texture is not None:
                        screen.blit(texture, (obj.points[0][0] - TILE_SIZE // 2, obj.points[0][1]))
                elif self.board[obj.y][obj.x] & Tile.ICE != 0:
                    screen.blit(TEXTURES['ICE'], (obj.points[0][0] - TILE_SIZE // 2, obj.points[0][1]))
                    if self.board[obj.y][obj.x] & Tile.PENGUIN != 0:
                        screen.blit(TEXTURES['PENGUIN'], (obj.points[0][0] - TILE_SIZE // 2, obj.points[0][1] - TILE_SIZE // 2))
                    
                elif self.board[obj.y][obj.x] & Tile.CRACKED_ICE != 0:
                    if obj.y == 1:
                        print(len(self.username), obj.x // 2)
                        print(self.username[obj.x // 2 - 1])
                        texture_pos = 'ICE_' + self.username[obj.x // 2 - 1].upper()
                        if texture_pos not in TEXTURES:
                            texture_pos = 'ICE_A'
                        screen.blit(TEXTURES[texture_pos], (obj.points[0][0] - TILE_SIZE // 2, obj.points[0][1]))


class Menu(Supervisor):
    def __init__(self):
        global OBJECT_ID
        global TEXTURES
        self.hex_size = 64
        self.board_size = (8, 15)
        self.platform_start = center_board(self.board_size, self.hex_size)
        self.board = create_board(self.board_size[1], self.board_size[0], 0)
        
        self.objects = dict()
        for y, row in enumerate(self.board):
            for x, tile in enumerate(row):
                if tile & Tile.ICE != 0 or tile & Tile.CRACKED_ICE != 0:
                    if tile & Tile.PENGUIN != 0:
                        self.penguin_pos = (x, y)
                        self.penguin_id = OBJECT_ID
                    self.objects[OBJECT_ID] = Hexagon(
                        self.platform_start, x, y, 
                        self.hex_size, OBJECT_ID)
                    OBJECT_ID += 1
                
        self.username = Username()
    
    def handle_key(self, key):
        if key == 8:
            self.username.pop()
        if (key >= 97 and key <= 122) or (key >= 48 and key <= 57):
            self.username.push(chr(key))
        print(self.username.username)

    def used_ids(self):
        return self.objects.keys()
    
    def draw(self, screen: pygame.Surface):
        self.username.draw(screen)
        for obj in self.objects.values():
            # pygame.draw.polygon(screen, obj.color, obj.points)
            pass
    def handle_click(self, x, y, obj_id):
        pass
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
        self.start_pos = (center_board((16, 3), TILE_SIZE)[0], 0)
        for y, row in enumerate(self.board):
            for x, tile in enumerate(row):
                self.objects[OBJECT_ID] = Hexagon(
                    self.start_pos, x, y, 
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

    def first_obj_coords(self) -> tuple:
        return (self.start_pos[0], self.start_pos[1] + TILE_SIZE // 2)

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
                        texture_pos = 'ICE_' + self.username[obj.x // 2 - 1].upper()
                        if texture_pos not in TEXTURES:
                            texture_pos = 'ICE_A'
                        screen.blit(TEXTURES[texture_pos], (obj.points[0][0] - TILE_SIZE // 2, obj.points[0][1]))

class Button:
    def __init__(self, pos: tuple, textures: list):
        global OBJECT_ID
        self.button_id = None
        self.objects = dict()
        self.board = create_board(3, 3, 0, with_penguin=False)
        for y, row in enumerate(self.board):
            for x, tile in enumerate(row):
                if tile & Tile.ICE != 0:
                    self.objects[OBJECT_ID] = Hexagon(
                        pos, x, y, 
                        TILE_SIZE, OBJECT_ID)
                    if x == 2 and y == 1:
                        self.button_id = OBJECT_ID
                    OBJECT_ID += 1
        self.texture_idx = 0
        self.textures = textures
        self.texture_start = 0
        self.enable = True
    
    
    def handle_click(self, x, y, obj_id):
        if obj_id == self.button_id and self.enable:
            self.texture_idx = (self.texture_idx + 1) % (len(self.textures) - self.texture_start)
        

    def draw(self, screen: pygame.Surface):
        for obj in self.objects.values():
            if type(obj) == Hexagon:
                if self.board[obj.y][obj.x] & Tile.FINISH != 0:
                    texture = snow_texture(self.board, obj.x, obj.y)
                    if texture is not None:
                        screen.blit(texture, (obj.points[0][0] - TILE_SIZE // 2, obj.points[0][1]))
                elif self.board[obj.y][obj.x] & Tile.ICE != 0:
                    screen.blit(self.textures[self.texture_start + self.texture_idx], (obj.points[0][0] - TILE_SIZE // 2, obj.points[0][1]))


class GameType:
    ONLINE = 0
    LOCAL = 1

class Menu(Supervisor):
    def __init__(self):
        global OBJECT_ID
        global TEXTURES
        global TILE_SIZE
        self.objects = dict()
        self.username = Username()
        self.online_button = Button(
            (self.username.start_pos[0], 2 * TILE_SIZE), 
            [TEXTURES['ICON_ONLINE'], TEXTURES['ICON_ONLINE_SELECTED']]
            )
        self.local_button = Button(
            (self.username.start_pos[0] + 3 * TILE_SIZE, 2 * TILE_SIZE), 
            [TEXTURES['ICON_LOCAL'], TEXTURES['ICON_LOCAL_SELECTED']]
            )
        self.local_button.texture_idx = 1
        self.diff_button = Button(
            (self.username.start_pos[0] + 6.5 * TILE_SIZE, 2 * TILE_SIZE), 
            [
                TEXTURES['ICON_DIFF_UNSEL'],
                TEXTURES['ICON_DIFF_EASY'], 
                TEXTURES['ICON_DIFF_NORM'], 
                TEXTURES['ICON_DIFF_HARD']
            ]
        )
        self.diff_button.texture_idx = 1
        self.diff_button.texture_start = 1
        self.start_button = Button(
            (self.username.start_pos[0] + 10 * TILE_SIZE, 2 * TILE_SIZE), 
            [TEXTURES['ICON_START']]
        )
        self.exit_button = Button(
            (self.username.start_pos[0] + 13 * TILE_SIZE, 2 * TILE_SIZE), 
            [TEXTURES['ICON_EXIT']]
        )
        self.objects[self.exit_button.button_id] = self.exit_button
        self.objects[self.start_button.button_id] = self.start_button
        self.objects[self.online_button.button_id] = self.online_button
        self.objects[self.local_button.button_id] = self.local_button
        self.objects[self.diff_button.button_id] = self.diff_button
        self.game_type = GameType.LOCAL
    
    def handle_key(self, key):
        if key == 8:
            self.username.pop()
        if (key >= 97 and key <= 122) or (key >= 48 and key <= 57):
            self.username.push(chr(key))

    def used_ids(self):
        return self.objects.keys()
    
    def draw(self, screen: pygame.Surface):
        self.username.draw(screen)
        # for obj in self.objects.values():
        #     # pygame.draw.polygon(screen, obj.color, obj.points)
        #     # pass
        #     if type(obj) == Hexagon:
        #         if self.online_board[obj.y][obj.x] & Tile.FINISH != 0:
        #             texture = snow_texture(self.online_board, obj.x, obj.y)
        #             if texture is not None:
        #                 screen.blit(texture, (obj.points[0][0] - TILE_SIZE // 2, obj.points[0][1]))
        #         elif self.online_board[obj.y][obj.x] & Tile.ICON_ONLINE != 0:
        #             if self.game_type == GameType.ONLINE:
        #                 screen.blit(TEXTURES['ICON_ONLINE_SELECTED'], (obj.points[0][0] - TILE_SIZE // 2, obj.points[0][1]))
        #             else:
        #                 screen.blit(TEXTURES['ICON_ONLINE'], (obj.points[0][0] - TILE_SIZE // 2, obj.points[0][1]))
        #         elif self.online_board[obj.y][obj.x] & Tile.ICE != 0:
        #             screen.blit(TEXTURES['ICE'], (obj.points[0][0] - TILE_SIZE // 2, obj.points[0][1]))
        #         if self.online_board[obj.y][obj.x] & Tile.PENGUIN != 0:
        #             screen.blit(TEXTURES['PENGUIN'], (obj.points[0][0] - TILE_SIZE // 2, obj.points[0][1] - TILE_SIZE // 2))
        self.online_button.draw(screen)
        self.local_button.draw(screen)
        self.diff_button.draw(screen)
        self.exit_button.draw(screen)
        self.start_button.draw(screen)
    
    def handle_click(self, x, y, obj_id):
        if type(self.objects[obj_id]) == Button:
            if obj_id == self.online_button.button_id:
                self.game_type = GameType.ONLINE
                self.local_button.texture_idx = 1 - self.local_button.texture_idx
            elif obj_id == self.local_button.button_id:
                self.game_type = GameType.LOCAL
                self.online_button.texture_idx = 1 - self.online_button.texture_idx
            elif obj_id == self.exit_button.button_id:
                pygame.quit()
            
            
            self.objects[obj_id].handle_click(x, y, obj_id)
            if obj_id != self.diff_button.button_id:
                if self.online_button.texture_idx == 1:
                    self.diff_button.texture_start = 0
                    self.diff_button.texture_idx = 0
                    self.diff_button.enable = False
                elif self.local_button.texture_idx == 1:
                    self.diff_button.texture_start = 1
                    self.diff_button.enable = True
            
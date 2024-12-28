
from .penguin_engine import Hexagon, create_board, Tile, snow_texture
from .gui_params import TILE_SIZE, index_buffer
import pygame

class Button:
    def __init__(self, pos: tuple, textures: list):
        global index_buffer
        self.button_id = None
        self.objects = dict()
        self.board = create_board(3, 3, 0, with_penguin=False)
        for y, row in enumerate(self.board):
            for x, tile in enumerate(row):
                if tile & Tile.ICE != 0:
                    self.objects[index_buffer.object_id] = Hexagon(
                        pos, x, y, 
                        TILE_SIZE, index_buffer.object_id)
                    if x == 2 and y == 1:
                        self.button_id = index_buffer.object_id
                    index_buffer.object_id += 1
        self.texture_idx = 0
        self.textures = textures
        self.texture_start = 0
        self.enable = True
    
    def get_state(self):
        return self.texture_idx

    def handle_click(self, x, y, obj_id):
        if obj_id == self.button_id and self.enable:
            self.texture_idx = (self.texture_idx + 1) % (len(self.textures) - self.texture_start)  

    def animate(self):
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

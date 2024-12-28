
from .penguin_engine import Hexagon, create_board, Tile, snow_texture
from .gui_params import TILE_SIZE, index_buffer, assests
import pygame

class TextAlign:
    LEFT = 0
    RIGHT = 1
    CENTER = 2

class TextField:
    def __init__(
            self, 
            x: int, 
            y: int, 
            text: str, 
            font_size: int = 30, 
            font_color: int | tuple = 0x000000,
            align: int = TextAlign.LEFT
            ):
        self.align = align
        self.text = text
        self.font = pygame.font.Font(assests.font_path, font_size)
        self.display_text = self.font.render(self.text, True, font_color)
        self.width = self.display_text.get_width()
        self.height = self.display_text.get_height()
        if self.align == TextAlign.RIGHT:
            x = x - (3 + self.width // TILE_SIZE) * TILE_SIZE

        self.origin = (x, y)
        self.x = (2 * x + (3 + self.width // TILE_SIZE) * TILE_SIZE) // 2 - self.width // 2
        self.y = (2 * y + 3 * TILE_SIZE) // 2 - self.height

        self.background = create_board(3, 3 + self.width // TILE_SIZE, 0)
        self.background_board = []
        for y_, row in enumerate(self.background):
            for x_, tile in enumerate(row):
                self.background_board.append(Hexagon(
                        self.origin, x_, y_, 
                        TILE_SIZE, index_buffer.object_id))

    def draw(self, screen: pygame.Surface):

        # Draw background
        for hex in self.background_board:
            if (self.background[hex.y][hex.x] & Tile.ICE != 0 and 
                self.background[hex.y][hex.x] & Tile.FINISH != 0):
                screen.blit(snow_texture(self.background, hex.x, hex.y), (hex.points[0][0] - TILE_SIZE / 2, hex.points[0][1]))
            elif self.background[hex.y][hex.x] & Tile.ICE:    
                screen.blit(assests.textures['ICE_CLEAN'], (hex.points[0][0] - TILE_SIZE / 2, hex.points[0][1]))
            
                    
        # if self.align == TextAlign.RIGHT:
        #     screen.blit(self.display_text, (self.x - self.width, self.y))
        # else:
        screen.blit(self.display_text, (self.x, self.y))
        
        

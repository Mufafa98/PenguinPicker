"""
### About
This module contains the TextField class, which is used to display 
text on the screen, mainly for usernames.
### Classes
- `TextField`: This class is used to display text on the screen.
- `TextAlign`: This class is used to align the text in the TextField.
"""

from .penguin_engine import Hexagon, create_board, Tile, snow_texture
from .gui_params import TILE_SIZE, index_buffer, assets
import pygame


class TextAlign:
    """
    ### About
    - This class is used to align the text in the TextField.
    ### Attributes
    - `LEFT`: Aligns the text to the left.
    - `RIGHT`: Aligns the text to the right.
    - `CENTER`: Aligns the text to the center.
    """
    LEFT = 0
    RIGHT = 1
    CENTER = 2


class TextField:
    """
    ### About
    - This class is used to display text on the screen.
    ### Attributes
    - `align`: Aligns the text in the TextField.
    - `text`: The text to be displayed.
    - `font`: The font of the text.
    - `display_text`: The rendered text.
    - `width`: The width of the text.
    - `height`: The height of the text.
    - `origin`: The origin of the object.
    - `x`: The x-coordinate of the text.
    - `y`: The y-coordinate of the text.
    - `background`: The background of the text.
    - `background_board`: The background board of the text.
    ### Methods
    - `draw(screen)`: Draws the text on the screen.
    """
    def __init__(self, x: int, y: int, text: str,
                 font_size: int = 30,
                 font_color: int | tuple = 0x000000,
                 align: int = TextAlign.LEFT):
        """
        ### About
        - Initializes the TextField object.
        ### Parameters
        - `x`: The x-coordinate of the text.
        - `y`: The y-coordinate of the text.
        - `text`: The text to be displayed.
        - `font_size`: The size of the font.
        - `font_color`: The color of the font.
        - `align`: Aligns the text in the TextField.
        """
        self.align = align
        self.text = text
        self.font = pygame.font.Font(assets.font_path, font_size)
        self.display_text = self.font.render(self.text, True, font_color)
        self.width = self.display_text.get_width()
        self.height = self.display_text.get_height()
        # Align object to the Right
        if self.align == TextAlign.RIGHT:
            x = x - (3 + self.width // TILE_SIZE) * TILE_SIZE

        self.origin = (x, y)
        self.x = (2 * x + 3 * TILE_SIZE + self.width) // 2 - self.width // 2
        self.y = (2 * y + 3 * TILE_SIZE) // 2 - self.height

        self.background = create_board(3, 3 + self.width // TILE_SIZE, 0)
        self.background_board = []
        for y_, row in enumerate(self.background):
            for x_, tile in enumerate(row):
                self.background_board.append(
                    Hexagon(
                        self.origin, x_, y_,
                        TILE_SIZE, index_buffer.object_id
                    )
                )

    def draw(self, screen: pygame.Surface):
        """
        ### About
        - Draws the text on the screen.
        ### Parameters
        - `screen`: The screen to draw the text on.
        """
        for hex in self.background_board:
            tile = self.background[hex.y][hex.x]
            if (tile & Tile.ICE != 0 and tile & Tile.FINISH != 0):
                screen.blit(
                    snow_texture(self.background, hex.x, hex.y),
                    (hex.points[0][0] - TILE_SIZE / 2, hex.points[0][1])
                )
            elif self.background[hex.y][hex.x] & Tile.ICE:
                screen.blit(
                    assets.textures['ICE_CLEAN'],
                    (hex.points[0][0] - TILE_SIZE / 2, hex.points[0][1])
                )
        screen.blit(self.display_text, (self.x, self.y))

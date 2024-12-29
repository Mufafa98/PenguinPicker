"""
### About
- This module defines a button class that is used to create buttons in the GUI.
"""
from .hex_utils import create_board, snow_texture
from .hexagon import Hexagon, Tile
from .gui_params import TILE_SIZE, index_buffer
import pygame


class Button:
    """
    ### About
    - This class represents a button in the GUI.
    ### Methods
    - `handle_click(x, y, obj_id)`: Handles a click event.
    - `set_state(state)`: Sets the button state.
    - `get_state()`: Gets the button state.
    - `animate()`: Animates the button.
    - `draw(screen)`: Draws the button on the screen.
    ### Atributes
    - `button_id`: The id of the button.
    - `objects`: A dictionary containing the objects that make up the button.
    - `board`: The board representing the background of the button.
    - `texture_idx`: The index of the texture to be displayed.
    - `textures`: A list of textures that can be displayed.
    - `texture_start`: The index of the first texture to be displayed.
    """
    def __init__(self, pos: tuple, textures: list):
        """
        ### About
        - Initializes the button.
        ### Parameters
        - `pos`: The position of the button.
        - `textures`: A list of textures that can be displayed.
        """
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

    def handle_click(self, x, y, obj_id):
        """
        ### About
        - Handles a click event.
        ### Parameters
        - `x`: The x coordinate of the click.
        - `y`: The y coordinate of the click.
        - `obj_id`: The id of the object that was clicked.
        """
        if obj_id == self.button_id and self.enable:
            self.texture_idx = (
                (self.texture_idx + 1) %
                (len(self.textures) - self.texture_start)
            )

    def set_state(self, state):
        """
        ### About
        - Sets the button state, and the texture index.
        """
        self.texture_idx = state

    def get_state(self):
        """
        ### About
        - Gets the button state.
        """
        return self.texture_idx

    def animate(self):
        """
        ### About
        - Animates the button by iterating through the textures.
        """
        self.texture_idx = (
            (self.texture_idx + 1) %
            (len(self.textures) - self.texture_start)
        )

    def draw(self, screen: pygame.Surface):
        """
        ### About
        - Draws the button on the screen.
        ### Parameters
        - `screen`: The screen to draw the button on.
        """
        for obj in self.objects.values():
            if isinstance(obj, Hexagon):
                obj_origin = obj.points[0]
                if self.board[obj.y][obj.x] & Tile.FINISH != 0:
                    texture = snow_texture(self.board, obj.x, obj.y)
                    if texture is not None:
                        screen.blit(
                            texture,
                            (
                                obj_origin[0] - TILE_SIZE // 2,
                                obj_origin[1]
                            )
                        )
                elif self.board[obj.y][obj.x] & Tile.ICE != 0:
                    screen.blit(
                        self.textures[self.texture_start + self.texture_idx],
                        (
                            obj_origin[0] - TILE_SIZE // 2,
                            obj_origin[1]
                        )
                    )

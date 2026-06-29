"""
### About
- Contains the global parameters for the GUI.
### Constants
- `TILE_SIZE`: The size of a tile.
- `BACKGROUND_COLOR`: The background color of the GUI.
- `SCREEN_SIZE`: The size of the screen.
- `FPS`: The frames per second.
### Classes
- `GameState`: A class to store the game state.
- `IndexBuffer`: A class to store the index buffer.
- `Assests`: A class to store the assets.
### Global Variables
- `game_state`: The game state.
- `index_buffer`: The index buffer.
- `assets`: The assets.
### Functions
- `load_assets`: Loads the assets.
### Supervisor Abstract Class
- `Supervisor`: An abstract class for the supervisors.
    - `handle_click`: An abstract method to handle a click.
"""
import logging

import pygame
import os


TILE_SIZE = 64
"""The size of a tile."""

BACKGROUND_COLOR = 0xF3F3F3
"""The background color of the GUI."""
SCREEN_SIZE = (TILE_SIZE * 18, TILE_SIZE * 14)
"""The size of the screen. Calculated baased on the tile size."""
FPS = 60
"""The frames per second."""


class GameState:
    """
    ### About
    - A class to store the game state.
    ### Attributes
    - `running`: A boolean to check if the game is running.
    - `game_type`: The type of the game. (Local / Online)
    - `game_turn`: The turn of the game. (Player 1 / Player 2)
    - `engine_reset`: A boolean to check if the engine has to be reset.
    - `menu_reset`: A boolean to check if the menu has to be reset.
    - `seed`: The seed of the game. Needed for board generation.
    - `player_1`: The name of player 1.
    - `player_2`: The name of player 2.
    - `game_difficulty`: The difficulty of the game. (Easy / Medium / Hard)
    """
    def __init__(self):
        """
        ### About
        - Initializes the game state.
        """
        self.running = False
        self.game_type = None
        self.game_turn = None
        self.engine_reset = False
        self.menu_reset = False
        self.seed = None
        self.player_1 = None
        self.player_2 = None
        self.game_difficulty = 0


game_state = GameState()
"""The game state."""


class IndexBuffer:
    """
    ### About
    - A class to store the index buffer.
    ### Attributes
    - `buffer`: A 2D list to store the objects ids.
    - `object_id`: A counter responsable for generating object ids.
    ### Methods
    - `restart_buffer`: Resets the buffer.
    ### Credit
    - Alex Mitreanu - (Yorknez)
    """
    def __init__(self):
        """
        ### About
        - Initializes the buffer.
        """
        self.buffer = [
            [
                [] for _ in range(0, SCREEN_SIZE[0])
            ] for _ in range(0, SCREEN_SIZE[1])
        ]
        self.object_id = 0

    def restart_buffer(self):
        """
        ### About
        - Resets the buffer.
        """
        self.buffer = [
            [
                [] for _ in range(0, SCREEN_SIZE[0])
            ] for _ in range(0, SCREEN_SIZE[1])
        ]
        self.object_id = 0


index_buffer = IndexBuffer()
"""The index buffer."""


class Assets:
    """
    ### About
    - A class to store the assets.
    ### Attributes
    - `textures`: A dictionary to store the textures.
    - `font_path`: The path to the used font.
    """
    def __init__(self):
        self.textures = dict()
        self.font_path = "./assets/fonts/04B_30__.TTF"


assets = Assets()


def load_assets(hex_size: int):
    """
    ### About
    - Loads the assets.
    ### Parameters
    - `hex_size`: The size of a hex tile.
    """
    global assets
    assets_dir = './assets/32x32'
    for subdir, _, files in os.walk(assets_dir):
        for file in files:
            if file.endswith('.png'):
                # texture = pygame.image.load(os.path.join(subdir, file))
                try:
                    texture = pygame.image.load(os.path.join(subdir, file))
                    # On certain systems, removing this line results in loosing
                    # the alpha channel from assets
                    texture.set_colorkey((0, 0, 0))
                except Exception as e:
                    logging.error(e)
                texture = pygame.transform.scale(texture, (hex_size, hex_size))
                texture_name = os.path.splitext(file)[0].upper()
                assets.textures[texture_name] = texture

class Supervisor:
    """
    ### About
    - An abstract class for the supervisors.
    - The supervisors are responsible for handling the clicks and hovers.
    ### Methods
    - `handle_click`: An abstract method to handle a click.
    """
    def handle_click(self, x: int, y: int, obj_id: int):
        """
        ### About
        - Handles a click.
        ### Parameters
        - `x`: The x coordinate of the click.
        - `y`: The y coordinate of the click.
        - `obj_id`: The id of the object
        ### Exceptions
        - `NotImplementedError`: If the method is not implemented by
        the subclass.
        """
        raise NotImplementedError("Method not implemented")

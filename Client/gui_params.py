import pygame
import os


TILE_SIZE = 64

BACKGROUND_COLOR = 0xF3F3F3
SCREEN_SIZE = (TILE_SIZE * 18, TILE_SIZE * 14)
FPS = 60


class GameState:
    def __init__(self):
        self.running = False
        self.game_type = None
        self.game_turn = None
        self.engine_reset = False
        self.menu_reset = False
        self.seed = None
        self.player_1 = None
        self.player_2 = None

game_state = GameState()

# INDEX BUFFER
# Credit: Alex Mitreanu
class IndexBuffer:
    def __init__(self):
        self.buffer = [
                [[] for _ in range(0, SCREEN_SIZE[0])] for _ in range(0, SCREEN_SIZE[1])
            ]
        self.object_id = 0

    def restart_buffer(self):
        self.buffer = [
                [[] for _ in range(0, SCREEN_SIZE[0])] for _ in range(0, SCREEN_SIZE[1])
            ]
        self.object_id = 0

index_buffer = IndexBuffer()    


class Assests:
    def __init__(self):
        self.textures = dict()
        self.font_path = "./assests/fonts/04B_30__.TTF"

assests = Assests()

# TEXTURES = dict()
# MAIN_FONT = None

def load_assets(hex_size: int) -> dict:
        global assests
        assets_dir = './assests/32x32'
        for subdir, _, files in os.walk(assets_dir):
            for file in files:
                if file.endswith('.png'):
                    texture = pygame.image.load(os.path.join(subdir, file))
                    texture = pygame.transform.scale(texture, (hex_size, hex_size))
                    texture_name = os.path.splitext(file)[0].upper()
                    assests.textures[texture_name] = texture
load_assets(TILE_SIZE)

class Supervisor:
    def handle_click(self, x: int, y: int, obj_id: int):
        raise NotImplementedError("Method not implemented")
    
    def handle_hover(self, x: int, y: int, obj_id: int):
        raise NotImplementedError("Method not implemented")
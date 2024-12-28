import pygame
import os

BACKGROUND_COLOR = 0xF3F3F3
SCREEN_SIZE = (1000, 800)
FPS = 60

TILE_SIZE = 64

# INDEX BUFFER
# Credit: Alex Mitreanu
index_buffer = [
    [[] for _ in range(0, SCREEN_SIZE[0])] for _ in range(0, SCREEN_SIZE[1])
]

TEXTURES = dict()
MAIN_FONT = None

def load_assets(hex_size: int) -> dict:
        global TEXTURES
        TEXTURES = dict()
        assets_dir = './assests/32x32'
        for subdir, _, files in os.walk(assets_dir):
            for file in files:
                if file.endswith('.png'):
                    texture = pygame.image.load(os.path.join(subdir, file))
                    texture = pygame.transform.scale(texture, (hex_size, hex_size))
                    texture_name = os.path.splitext(file)[0].upper()
                    TEXTURES[texture_name] = texture
load_assets(TILE_SIZE)
OBJECT_ID = 0

class Supervisor:
    def handle_click(self, x: int, y: int, obj_id: int):
        raise NotImplementedError("Method not implemented")
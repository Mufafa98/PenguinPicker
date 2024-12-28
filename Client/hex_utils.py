import random
import pygame
from .hexagon import Tile
from .gui_params import SCREEN_SIZE, assests

def create_board(
        lines: int, 
        cols: int, 
        crack_percent: float, 
        random_seed: int = None,
        penguin_pos: tuple = None, 
        with_penguin: bool = True) -> list:
    random.seed(random_seed)
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
    if with_penguin:
        if penguin_pos is None:
            mid_pos = (len(board[0]) // 2, len(board) // 2)
            if board[mid_pos[1]][mid_pos[0]] == Tile.EMPTY:
                mid_pos = (mid_pos[0] - 1, mid_pos[1])
            board[mid_pos[1]][mid_pos[0]] = Tile.ICE | Tile.PENGUIN
        else:
            board[penguin_pos[1]][penguin_pos[0]] = Tile.ICE | Tile.PENGUIN
    return board

def center_board(board_size: tuple, hex_size: int) -> tuple:
    board_width = board_size[0] * hex_size
    board_height = (((board_size[1] + 1 )/ 2) * hex_size + 
                    board_size[1] / 2 * hex_size / 2)
    return ((SCREEN_SIZE[0] - board_width) / 2, 
            (SCREEN_SIZE[1] - board_height) / 2)

def snow_texture(board: list, x: int, y: int) -> pygame.Surface:
        global assests
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
            return assests.textures['SNOW_BOTTOM']
        elif neighbors[0] == Tile.ICE and neighbors[4] == Tile.ICE:
            return assests.textures['SNOW_LEFT']
        elif neighbors[5] == Tile.ICE:
            return assests.textures['SNOW_SLEFT']
        elif neighbors[0] == Tile.ICE:
            return assests.textures['SNOW_BLEFT']
        elif neighbors[1] == Tile.ICE and neighbors[3] == Tile.ICE:
            return assests.textures['SNOW_RIGHT']
        elif neighbors[2] == Tile.ICE:
            return assests.textures['SNOW_SRIGHT']
        elif neighbors[1] == Tile.ICE:
            return assests.textures['SNOW_BRIGHT']
        elif neighbors[3] == Tile.ICE and neighbors[4] == Tile.ICE:
            return assests.textures['SNOW_TOP']
        elif neighbors[3] == Tile.ICE:
            return assests.textures['SNOW_TRIGHT']
        elif neighbors[4] == Tile.ICE:
            return assests.textures['SNOW_TLEFT']
        return None

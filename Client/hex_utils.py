"""
### About
- This module contains utility functions for the hexagon game.
### Functions
- `create_board()`: Creates a game board.
- `center_board()`: Returns a pair representing the coordonates where
the board should be placed to be centered on the screen.
- `snow_texture()`: Returns the snow texture for a hexagon.
- `hole_texture()`: Returns the hole texture for a hexagon.
"""

import random
import pygame
from .hexagon import Tile
from .gui_params import SCREEN_SIZE, assets


def create_board(
        lines: int,
        cols: int,
        crack_percent: float,
        random_seed: int = None,
        penguin_pos: tuple = None,
        with_penguin: bool = True) -> list:
    """
    ### About
    - This function creates a game board.
    ### Parameters
    - `lines`: The number of lines in the board.
    - `cols`: The number of columns in the board.
    - `crack_percent`: The percentage of cracked ice in the board.
    - `random_seed`: The seed for the random number generator.
    - `penguin_pos`: The position of the penguin.
    - `with_penguin`: If True, the penguin will be placed on the board
    otherwise it will be ignored.
    ### Returns
    - `list`: Representing the game board.
    """
    random.seed(random_seed)
    board = []
    for line in range(lines):
        temp_line = []
        for col in range(cols * 2 - 1):
            if (line + col) % 2 == 1:
                if (
                    line == 0
                    or line == lines - 1
                    or col <= 1
                    or col >= cols * 2 - 3
                ):
                    # The board should be bordered by snow tiles
                    # (by FINISH tiles)
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
    """
    ### About
    - This function returns a pair representing the coordonates where
    the board should be placed to be centered on the screen.
    ### Parameters
    - `board_size`: The size of the board.
    - `hex_size`: The size of a hexagon.
    ### Returns
    - `tuple`: The coordonates where the board should be placed.
    """
    board_width = board_size[0] * hex_size
    board_height = (
        ((board_size[1] + 1) / 2) * hex_size
        + board_size[1] / 2 * hex_size / 2)
    return ((SCREEN_SIZE[0] - board_width) / 2,
            (SCREEN_SIZE[1] - board_height) / 2)


def snow_texture(board: list, x: int, y: int) -> pygame.Surface:
    """
    ### About
    - This function returns the snow texture for a hexagon.
    ### Parameters
    - `board`: The game board.
    - `x`: The x coordinate of the hexagon.
    - `y`: The y coordinate of the hexagon.
    ### Returns
    - `pygame.Surface`: The snow texture.
    """
    global assets

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
        return assets.textures['SNOW_BOTTOM']
    elif neighbors[0] == Tile.ICE and neighbors[4] == Tile.ICE:
        return assets.textures['SNOW_LEFT']
    elif neighbors[5] == Tile.ICE:
        return assets.textures['SNOW_SLEFT']
    elif neighbors[0] == Tile.ICE:
        return assets.textures['SNOW_BLEFT']
    elif neighbors[1] == Tile.ICE and neighbors[3] == Tile.ICE:
        return assets.textures['SNOW_RIGHT']
    elif neighbors[2] == Tile.ICE:
        return assets.textures['SNOW_SRIGHT']
    elif neighbors[1] == Tile.ICE:
        return assets.textures['SNOW_BRIGHT']
    elif neighbors[3] == Tile.ICE and neighbors[4] == Tile.ICE:
        return assets.textures['SNOW_TOP']
    elif neighbors[3] == Tile.ICE:
        return assets.textures['SNOW_TRIGHT']
    elif neighbors[4] == Tile.ICE:
        return assets.textures['SNOW_TLEFT']
    return None


def hole_texture(board: list, x: int, y: int) -> pygame.Surface:
    """
    ### About
    - This function returns the hole texture for a hexagon.
    ### Parameters
    - `board`: The game board.
    - `x`: The x coordinate of the hexagon.
    - `y`: The y coordinate of the hexagon.
    ### Returns
    - `pygame.Surface`: The hole texture.
    """
    top_left_neigh = board[y - 1][x - 1]
    top_left_neigh = top_left_neigh & Tile.ICE
    top_right_neigh = board[y - 1][x + 1]
    top_right_neigh = top_right_neigh & Tile.ICE
    if top_left_neigh and top_right_neigh:
        return assets.textures['HOLE_HALF']
    elif top_left_neigh:
        return assets.textures['HOLE_HALF_LEFT']
    elif top_right_neigh:
        return assets.textures['HOLE_HALF_RIGHT']
    else:
        return assets.textures['HOLE_FULL']

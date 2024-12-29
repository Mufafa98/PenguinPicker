"""
### About
- This file contains the main game engine for the Penguin game.
- The engine is responsible for handling the game logic and rendering the game.
- The engine is also responsible for handling the user input and sending the 
moves to the server.
### Classes
- Engine: The main game engine class.
- Turn: Enum class for the turn types.
- GameStatus: Enum class for the game status.
"""

import pygame
import socket

from Utils.protocol import Protocol, Message

from .gui_params import Supervisor, index_buffer, assets, game_state
from .gui_params import SCREEN_SIZE, TILE_SIZE
from .game_type import GameType
from .hexagon import Hexagon, Tile
from .hex_utils import create_board, snow_texture, center_board, hole_texture
from .text_field import TextField, TextAlign
from .button import Button


class Turn:
    """
    ### About
    - Enum class for the turn types.
    ### Attributes
    - PENGUIN: The penguin's turn.
    - WALL: The wall's turn.
    """
    PENGUIN = 0b0
    WALL = 0b1


class GameStatus:
    """
    ### About
    - Enum class for the game status.
    ### Attributes
    - RUNNING: The game is running.
    - PENGUIN_WON: The penguin won the game.
    - CRACKER_WON: The cracker won the game.
    """
    RUNNING = 0b0
    PENGUIN_WON = 0b1
    CRACKER_WON = 0b10


class Engine(Supervisor):
    """
    ### About
    - The main game engine class.
    ### Methods
    - `handle_click(x: int, y: int, obj_id: int)`: Handles the user click.
    - `legal_for_penguin() -> bool`: Checks if the penguin can move.
    - `move_penguin(x: int, y: int, obj_id: int)`: Moves the penguin.
    - `place_wall(x: int, y: int, obj_id: int)`: Places a wall.
    - `used_ids() -> list`: Returns the used object ids.
    - `penguin_texture() -> pygame.Surface`: Returns the penguin texture.
    - `draw(screen: pygame.Surface)`: Draws the game on the screen.
    ### Attributes
    - `game_type`: The game type(Online or Offline).
    - `seed`: The seed for the random board generation.
    - `board_size`: The size of the board.
    - `hex_size`: The size of the hexagons.
    - `client_socket`: The client socket for the online game.
    - `allow_only`: The turn type allowed(PENGUIN or WALL).
    - `board`: The game board.
    - `hex_objects`: The hexagons on the board.
    - `platform_start`: The start position of the board.
    - `penguin_pos`: The position of the penguin.
    - `penguin_id`: The id of the penguin object.
    - `turn`: The current turn type.
    - `game_status`: The current game status.
    - `player_1`: The player 1 text field.
    - `player_2`: The player 2 text field.
    - `leave_button`: The leave button.

    """
    def __init__(self, game_type: GameType,
                 seed: int, board_size: tuple = (18, 15), hex_size: int = 64,
                 client_socket: socket.socket = None, allow_only: Turn = None,
                 player_1: str = "Anonymous", player_2: str = "Anonymous"):
        global index_buffer
        global assets
        global TILE_SIZE, SCREEN_SIZE
        self.allow_only = allow_only
        self.socket = client_socket
        self.seed = seed
        self.game_type = game_type
        self.board_size = board_size
        self.board = create_board(
            board_size[1],
            board_size[0],
            0.2,
            random_seed=seed
        )
        self.hex_size = hex_size
        self.platform_start = (center_board(board_size, hex_size)[0], 0)
        self.hex_objects = dict()
        for y, row in enumerate(self.board):
            for x, tile in enumerate(row):
                if tile & Tile.ICE != 0 or tile & Tile.CRACKED_ICE != 0:
                    if tile & Tile.PENGUIN != 0:
                        self.penguin_pos = (x, y)
                        self.penguin_id = index_buffer.object_id
                    self.hex_objects[index_buffer.object_id] = Hexagon(
                        self.platform_start, x, y,
                        hex_size, index_buffer.object_id)
                    index_buffer.object_id += 1
        self.turn = Turn.PENGUIN
        self.game_status = GameStatus.RUNNING
        self.player_1 = TextField(
            0,
            SCREEN_SIZE[1] - 3 * TILE_SIZE,
            player_1,
            font_color=(25, 129, 157)
        )
        self.player_2 = TextField(
            SCREEN_SIZE[0],
            SCREEN_SIZE[1] - 3 * TILE_SIZE,
            player_2,
            align=TextAlign.RIGHT,
            font_color=(38, 143, 172)
        )
        self.leave_button = Button(
            (
                SCREEN_SIZE[0] // 2 - 1.5 * TILE_SIZE,
                SCREEN_SIZE[1] - 3 * TILE_SIZE
            ),
            [
                assets.textures['ICON_LEFT_PLAYER'],
                assets.textures['ICON_RIGHT_PLAYER'],
                assets.textures['ICON_LEAVE_MATCH'],
                assets.textures['ICON_LOSE_PLAYER'],
                assets.textures['ICON_WIN_PLAYER']
            ]
        )

    def handle_click(self, x: int, y: int, obj_id: int):
        """
        ### About
        - Handles the user click.
        ### Parameters
        - `x`: The x position of the click.
        - `y`: The y position of the click.
        - `obj_id`: The id of the object clicked.
        """
        global game_state
        if obj_id in self.hex_objects:
            if self.game_status == GameStatus.RUNNING:
                if self.allow_only is None or self.allow_only == self.turn:
                    if self.turn == Turn.PENGUIN:
                        if self.move_penguin(x, y, obj_id):
                            # move was successful
                            message = Message(Protocol.PENGUIN, f"{x} {y}")
                            self.socket.sendall(message.to_bytes())
                    elif self.turn == Turn.WALL:
                        if self.place_wall(x, y, obj_id):
                            # wall was placed
                            message = Message(Protocol.WALL, f"{x} {y}")
                            self.socket.sendall(message.to_bytes())
        elif obj_id == self.leave_button.button_id:
            print("Leave button clicked")
            game_state.running = False
            game_state.menu_reset = True
            index_buffer.restart_buffer()
        else:
            print(f"Invalid click: Game Finished: {self.game_status}")

    def legal_for_penguin(self) -> bool:
        """
        ### About
        - Checks if the penguin can move.
        ### Returns
        - `bool`: True if the penguin can move, False otherwise.
        """
        def inside_board(x: int, y: int) -> bool:
            """
            ### About
            - Checks if the position is inside the board.
            """
            return 0 <= x < len(self.board[0]) and 0 <= y < len(self.board)
        penguin_obj = self.hex_objects[self.penguin_id]
        obj_x = penguin_obj.x
        obj_y = penguin_obj.y
        return (
            (
                inside_board(obj_x - 2, obj_y) and
                self.board[obj_y][obj_x - 2] & Tile.ICE != 0
            ) or (
                inside_board(obj_x + 2, obj_y) and
                self.board[obj_y][obj_x + 2] & Tile.ICE != 0
            ) or (
                inside_board(obj_x - 1, obj_y - 1) and
                self.board[obj_y - 1][obj_x - 1] & Tile.ICE != 0
            ) or (
                inside_board(obj_x + 1, obj_y - 1) and
                self.board[obj_y - 1][obj_x + 1] & Tile.ICE != 0
            ) or (
                inside_board(obj_x - 1, obj_y + 1) and
                self.board[obj_y + 1][obj_x - 1] & Tile.ICE != 0
            ) or (
                inside_board(obj_x + 1, obj_y + 1) and
                self.board[obj_y + 1][obj_x + 1] & Tile.ICE != 0
            )
        )

    def move_penguin(self, x: int, y: int, obj_id: int):
        """
        ### About
        - Moves the penguin to the new position.
        ### Parameters
        - `x`: The x position of the new position.
        - `y`: The y position of the new position.
        - `obj_id`: The id of the object clicked.
        """
        penguin_obj = self.hex_objects[self.penguin_id]
        current_obj = self.hex_objects[obj_id]

        curr_y = current_obj.y
        curr_x = current_obj.x

        # If the new possition is not ice or the penguin is too far
        # return False
        if self.board[curr_y][curr_x] & Tile.ICE == 0:
            return False
        if abs(penguin_obj.x - curr_x) > 2 or abs(penguin_obj.y - curr_y) > 1:
            return False

        aux = penguin_obj.color
        penguin_obj.color = current_obj.color
        current_obj.color = aux

        self.board[penguin_obj.y][penguin_obj.x] = Tile.ICE
        self.penguin_id = obj_id
        self.board[curr_y][curr_x] = Tile.PENGUIN | self.board[curr_y][curr_x]
        self.turn = Turn.WALL
        self.leave_button.texture_idx = 1
        if self.board[curr_y][curr_x] & Tile.FINISH != 0:
            self.game_status = GameStatus.PENGUIN_WON
        return True

    def place_wall(self, x: int, y: int, obj_id: int):
        """
        ### About
        - Places a wall on the board.
        ### Parameters
        - `x`: The x position of the wall.
        - `y`: The y position of the wall.
        - `obj_id`: The id of the object clicked.
        """
        curr_x = self.hex_objects[obj_id].x
        curr_y = self.hex_objects[obj_id].y
        tile = self.board[curr_y][curr_x]
        if (tile & Tile.PENGUIN != 0 or tile & Tile.FINISH != 0):
            return False
        self.board[curr_y][curr_x] = Tile.CRACKED_ICE
        self.hex_objects[obj_id].color = 0xA0A0A0
        self.turn = Turn.PENGUIN
        self.leave_button.texture_idx = 0
        if not self.legal_for_penguin():
            self.game_status = GameStatus.CRACKER_WON
        return True

    def used_ids(self) -> list:
        """
        ### About
        - Returns the used object ids.
        ### Returns
        - `list`: The used object ids.
        """
        temp = list(self.hex_objects.keys())
        temp.append(self.leave_button.button_id)
        return temp

    def penguin_texture(self) -> pygame.Surface:
        """
        ### About
        - Returns the penguin texture depending on the game status.
        ### Returns
        - `pygame.Surface`: The penguin texture.
        """
        global assets
        if self.game_status == GameStatus.PENGUIN_WON:
            return assets.textures['PENGUIN']
        elif self.legal_for_penguin():
            return assets.textures['PENGUIN_SCARED']
        return assets.textures['PENGUIN_SAD']

    def draw(self, screen: pygame.Surface):
        """
        ### About
        - Draws the game on the screen.
        ### Parameters
        - `screen`: The screen to draw on.
        """
        global assets
        try:
            # Set up a non-blocking socket to recieve the moves
            # that were made by the other player
            data = self.socket.recv(1024, socket.MSG_DONTWAIT)
            if data:
                message = Message.from_bytes(data)
                x, y = message.data.split()
                x = int(x)
                y = int(y)
                if message.protocol == Protocol.PENGUIN:
                    self.move_penguin(x, y, index_buffer.buffer[y][x])
                elif message.protocol == Protocol.WALL:
                    self.place_wall(x, y, index_buffer.buffer[y][x])
        except BlockingIOError:
            pass

        for hexagon in self.hex_objects.values():
            hex_origin = hexagon.points[0]
            if self.board[hexagon.y][hexagon.x] & Tile.CRACKED_ICE != 0:
                texture = hole_texture(self.board, hexagon.x, hexagon.y)
                if texture is not None:
                    screen.blit(
                        texture,
                        (hex_origin[0] - self.hex_size / 2,
                         hex_origin[1])
                    )
            elif (self.board[hexagon.y][hexagon.x] & Tile.ICE != 0 and
                  self.board[hexagon.y][hexagon.x] & Tile.FINISH == 0):
                screen.blit(
                    assets.textures['ICE'],
                    (hex_origin[0] - self.hex_size / 2,
                     hex_origin[1])
                )
            elif self.board[hexagon.y][hexagon.x] & Tile.FINISH != 0:
                texture = snow_texture(self.board, hexagon.x, hexagon.y)
                if texture is not None:
                    screen.blit(
                        texture,
                        (hex_origin[0] - self.hex_size / 2,
                         hex_origin[1])
                    )
            if hexagon.obj_id == self.penguin_id:
                screen.blit(
                    self.penguin_texture(),
                    (hex_origin[0] - self.hex_size / 2,
                     hex_origin[1] - self.hex_size * 0.25)
                )

        self.player_1.draw(screen)
        self.player_2.draw(screen)

        mouse_pos = pygame.mouse.get_pos()

        # Leave button animation
        if self.game_status == GameStatus.RUNNING:
            if (
                index_buffer.buffer[mouse_pos[1]][mouse_pos[0]] ==
                self.leave_button.button_id
            ):
                self.leave_button.texture_idx = 2
            else:
                self.leave_button.texture_idx = self.turn
        elif self.game_status == GameStatus.PENGUIN_WON:
            if self.allow_only == Turn.PENGUIN:
                self.leave_button.texture_idx = 4
            else:
                self.leave_button.texture_idx = 3
        elif self.game_status == GameStatus.CRACKER_WON:
            if self.allow_only == Turn.WALL:
                self.leave_button.texture_idx = 4
            else:
                self.leave_button.texture_idx = 3
        self.leave_button.draw(screen)

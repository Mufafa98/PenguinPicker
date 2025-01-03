"""
### About
- This module contains the `Menu` class which is responsable
for the main menu of the game.
"""

from .gui_params import Supervisor, TILE_SIZE
from .gui_params import index_buffer, assets, game_state
from .hex_utils import create_board, center_board, snow_texture
from .hexagon import Hexagon, Tile
import socket
import pygame
import random
from Utils import Message, Protocol
from .game_type import GameType
from .button import Button


class Username:
    """
    ### About
    - This class is responsable for handling the username input.
    - It draws an ice background and moves a penguin on it.
    ### Attributes
    - `username`: The current username string. (max 13 characters)
    - `penguin_pos`: The position of the penguin on the background.
    - `board`: The background of the username input.
    - `objects`: A dictionary containing the objects that need to be drawn.
    - `start_pos`: The starting position of the Username object.
    ### Methods
    - `pop`: Removes the last character from the username.
    - `push`: Adds a character to the username.
    - `draw`: Draws the username input on the screen.
    """
    def __init__(self):
        """
        ### About
        - This method initializes the `Username` object.
        """
        global index_buffer
        global TILE_SIZE
        self.username = ""
        self.penguin_pos = (2, 1)
        # A username can be at most 16 - 2 - 1 = 13 characters long
        self.board = create_board(3, 16, 0, penguin_pos=self.penguin_pos)
        self.objects = dict()
        self.start_pos = (center_board((16, 3), TILE_SIZE)[0], 0)
        for y, row in enumerate(self.board):
            for x, tile in enumerate(row):
                self.objects[index_buffer.object_id] = Hexagon(
                    self.start_pos, x, y,
                    TILE_SIZE, index_buffer.object_id)
                index_buffer.object_id += 1

    def pop(self):
        """
        ### About
        - This method removes the last character from the username.
        - Moves the penguin to the left.
        """
        self.username = self.username[:-1]
        if self.penguin_pos[0] - 2 < 1:
            return
        penguin_x = self.penguin_pos[0]
        penguin_y = self.penguin_pos[1]
        self.board[penguin_y][penguin_x] = Tile.ICE
        self.board[penguin_y][penguin_x - 2] = Tile.ICE | Tile.PENGUIN
        self.penguin_pos = (penguin_x - 2, penguin_y)

    def push(self, char):
        """
        ### About
        - This method adds a character to the username.
        - Moves the penguin to the right.
        ### Parameters
        - `char`: The character to be added to the username.
        """
        if self.penguin_pos[0] + 2 >= len(self.board[0]) - 1:
            return
        penguin_x = self.penguin_pos[0]
        penguin_y = self.penguin_pos[1]
        self.username += char
        self.board[penguin_y][penguin_x] = Tile.CRACKED_ICE
        self.board[penguin_y][penguin_x + 2] |= Tile.PENGUIN
        self.penguin_pos = (penguin_x + 2, penguin_y)

    def draw(self, screen: pygame.Surface):
        """
        ### About
        - This method draws the username input on the screen.
        ### Parameters
        - `screen`: The surface on which the username input will be drawn.
        """
        global assets
        for obj in self.objects.values():
            if isinstance(obj, Hexagon):
                obj_origin = obj.points[0]
                tile = self.board[obj.y][obj.x]
                if tile & Tile.FINISH != 0:
                    texture = snow_texture(self.board, obj.x, obj.y)
                    if texture is not None:
                        screen.blit(
                            texture,
                            (
                                obj_origin[0] - TILE_SIZE // 2,
                                obj_origin[1]
                            )
                        )
                elif tile & Tile.ICE != 0:
                    screen.blit(
                        assets.textures['ICE'],
                        (
                            obj_origin[0] - TILE_SIZE // 2,
                            obj_origin[1]
                        )
                    )
                    if tile & Tile.PENGUIN != 0:
                        screen.blit(
                            assets.textures['PENGUIN'],
                            (
                                obj_origin[0] - TILE_SIZE // 2,
                                obj_origin[1] - TILE_SIZE // 2
                            )
                        )

                elif tile & Tile.CRACKED_ICE != 0:
                    if obj.y == 1:
                        texture_pos = 'ICE_'
                        texture_pos += self.username[obj.x // 2 - 1].upper()
                        if texture_pos not in assets.textures:
                            texture_pos = 'ICE_A'
                        screen.blit(
                            assets.textures[texture_pos],
                            (
                                obj_origin[0] - TILE_SIZE // 2,
                                obj_origin[1]
                            )
                        )


class Menu(Supervisor):
    """
    ### About
    - This class is responsable for the main menu of the game.
    ### Attributes
    - `waiting`: A boolean flag that indicates if the game is waiting for
    the server to start the game.
    - `socket`: The socket object used to communicate with the server.
    - `objects`: A dictionary containing the objects that need to be drawn.
    - `username`: The username input object.
    - `online_button`: The button that switches the game type to online.
    - `local_button`: The button that switches the game type to local.
    - `diff_button`: The button that switches the difficulty of the game.
    (easy, normal, hard)
    - `start_button`: The button that starts the game.
    - `exit_button`: The button that exits the game.
    - `game_type`: The current game type.
    - `counter`: A counter used to animate the start button.
    ### Methods
    - `handle_key`: Handles the key events.
    - `handle_click`: Handles the click events.
    - `used_ids`: Returns the ids of the objects that ware used.
    - `draw`: Draws the menu on the screen.
    """
    def __init__(self, client_socket: socket.socket):
        global assets
        global TILE_SIZE
        self.waiting = False
        self.socket = client_socket
        self.objects = dict()
        self.username = Username()
        self.online_button = Button(
            (self.username.start_pos[0], 2 * TILE_SIZE),
            [
                assets.textures['ICON_ONLINE'],
                assets.textures['ICON_ONLINE_SELECTED']
            ]
        )
        self.local_button = Button(
            (self.username.start_pos[0] + 3 * TILE_SIZE, 2 * TILE_SIZE),
            [
                assets.textures['ICON_LOCAL'],
                assets.textures['ICON_LOCAL_SELECTED']
            ]
        )
        self.local_button.texture_idx = 1
        self.diff_button = Button(
            (self.username.start_pos[0] + 6.5 * TILE_SIZE, 2 * TILE_SIZE),
            [
                assets.textures['ICON_DIFF_UNSEL'],
                assets.textures['ICON_DIFF_EASY'],
                assets.textures['ICON_DIFF_NORM'],
                assets.textures['ICON_DIFF_HARD']
            ]
        )
        self.diff_button.texture_idx = 1
        self.diff_button.texture_start = 1
        self.start_button = Button(
            (self.username.start_pos[0] + 10 * TILE_SIZE, 2 * TILE_SIZE),
            [
                assets.textures['ICON_START'],
                assets.textures['ICON_START_1'],
                assets.textures['ICON_START_2'],
                assets.textures['ICON_START_3'],
                assets.textures['ICON_START_4'],
                assets.textures['ICON_START_5']
            ]
        )
        self.exit_button = Button(
            (self.username.start_pos[0] + 13 * TILE_SIZE, 2 * TILE_SIZE),
            [
                assets.textures['ICON_EXIT']
            ]
        )
        self.objects[self.exit_button.button_id] = self.exit_button
        self.objects[self.start_button.button_id] = self.start_button
        self.objects[self.online_button.button_id] = self.online_button
        self.objects[self.local_button.button_id] = self.local_button
        self.objects[self.diff_button.button_id] = self.diff_button
        self.game_type = GameType.LOCAL
        self.counter = 0

    def handle_key(self, key):
        """
        ### About
        - This method handles the key events.(Only if the start button
        was not pressed)
        ### Parameters
        - `key`: The key code of the pressed key.
        """
        if not self.waiting:
            if key == 8:
                # Backspace
                self.username.pop()
            if (key >= 97 and key <= 122) or (key >= 48 and key <= 57):
                # Letters and numbers
                self.username.push(chr(key))

    def handle_click(self, x, y, obj_id):
        """
        ### About
        - This method handles the click events.
        ### Parameters
        - `x`: The x coordinate of the click.
        - `y`: The y coordinate of the click.
        - `obj_id`: The id of the object that was clicked.
        """
        if isinstance(self.objects[obj_id], Button):
            if obj_id == self.online_button.button_id:
                self.game_type = GameType.ONLINE
                # We don't want to have both local and
                # online buttons selected, so we deselect the other one
                self.local_button.set_state(
                    1 - self.local_button.get_state()
                )
            elif obj_id == self.local_button.button_id:
                self.game_type = GameType.LOCAL
                # We don't want to have both local and
                # online buttons selected, so we deselect the other one
                self.online_button.set_state(
                    1 - self.online_button.get_state()
                )
            elif obj_id == self.exit_button.button_id:
                message = Message(Protocol.EXIT, "")
                self.socket.sendall(message.to_bytes())
                pygame.quit()
            elif obj_id == self.start_button.button_id:
                if self.game_type == GameType.ONLINE:
                    message = Message(
                        Protocol.START,
                        f"{self.username.username}"
                    )
                    self.socket.sendall(message.to_bytes())
                    self.waiting = True
                elif self.game_type == GameType.LOCAL:
                    global game_state
                    game_state.running = True
                    game_state.game_type = self.game_type
                    game_state.engine_reset = True
                    game_state.seed = random.randint(0, 1000000)
                    if self.username.username == "penguin":
                        game_state.game_turn = 0
                        game_state.player_1 = self.username.username
                        game_state.player_2 = "BOT"
                    elif self.username.username == "cracker":
                        game_state.game_turn = 1
                        game_state.player_1 = "BOT"
                        game_state.player_2 = self.username.username
                    else:
                        game_state.game_turn = random.randint(0, 1)
                        if game_state.game_turn == 0:
                            game_state.player_1 = self.username.username
                            game_state.player_2 = "BOT"
                        else:
                            game_state.player_1 = "BOT"
                            game_state.player_2 = self.username.username
                    game_state.game_difficulty = self.diff_button.get_state()

            # If the online button is not selected, disable
            # the difficulty button, otherwise enable it
            # and set the correct texture interval
            self.objects[obj_id].handle_click(x, y, obj_id)
            if obj_id != self.diff_button.button_id:
                if self.online_button.get_state() == 1:
                    self.diff_button.texture_start = 0
                    self.diff_button.set_state(0)
                    self.diff_button.enable = False
                elif self.local_button.get_state() == 1:
                    self.diff_button.texture_start = 1
                    self.diff_button.enable = True
            # Update the game state
            if self.online_button.get_state() == 1:
                self.game_type = GameType.ONLINE
            else:
                self.game_type = GameType.LOCAL

    def used_ids(self):
        """
        ### About
        - This method returns the ids of the objects that ware used.
        ### Returns
        - A list containing the ids of the objects that ware used.
        """
        return self.objects.keys()

    def draw(self, screen: pygame.Surface):
        """
        ### About
        - This method draws the menu on the screen.
        ### Parameters
        - `screen`: The surface on which the menu will be drawn.
        ### Exceptions
        - `ValueError`: If the message data recived from the server
        does not have the correct format.
        """
        self.username.draw(screen)
        self.online_button.draw(screen)
        self.local_button.draw(screen)
        self.diff_button.draw(screen)
        self.exit_button.draw(screen)
        self.start_button.draw(screen)

        if self.waiting:
            self.counter = self.counter + 1
            if self.counter % 10 == 0:
                self.start_button.animate()
            try:
                # Set up a non blocking reciveing socket
                # that has to detect if the server has started the game
                data = self.socket.recv(1024, socket.MSG_DONTWAIT)
                if data:
                    message = Message.from_bytes(data)
                    print(f"Message: {message}")
                    if message.protocol == Protocol.START:
                        print("Starting game")
                        global game_state
                        game_state.running = True
                        game_state.game_type = self.game_type
                        game_state.engine_reset = True
                        params = message.data.split()
                        if len(params) == 4:
                            game_state.seed = int(params[0])
                            game_state.game_turn = int(params[1])
                            game_state.player_1 = params[2]
                            game_state.player_2 = params[3]
                        else:
                            raise ValueError("Invalid message data")
                        self.waiting = False
            except BlockingIOError:
                pass
            except Exception as e:
                print(e)
                self.waiting = False

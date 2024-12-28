from .gui_params import *
from .hex_utils import create_board, center_board, snow_texture
from .hexagon import Hexagon, Tile
import socket
import pygame
from Utils import Message, Protocol
from .game_type import GameType
from .button import Button


class Username:
    def __init__(self):
        global index_buffer
        global TILE_SIZE
        self.username = ""
        self.penguin_pos = (2, 1)
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
        self.username = self.username[:-1]
        if self.penguin_pos[0] - 2 < 1:
            return
        self.board[self.penguin_pos[1]][self.penguin_pos[0]] = Tile.ICE
        self.board[self.penguin_pos[1]][self.penguin_pos[0] - 2] =Tile.ICE | Tile.PENGUIN
        self.penguin_pos = (self.penguin_pos[0] - 2, self.penguin_pos[1])
    
    def push(self, char):
        if self.penguin_pos[0] + 2 >= len(self.board[0]) - 1:
            return
        self.username += char
        self.board[self.penguin_pos[1]][self.penguin_pos[0]] = Tile.CRACKED_ICE
        self.board[self.penguin_pos[1]][self.penguin_pos[0] + 2] |= Tile.PENGUIN
        self.penguin_pos = (self.penguin_pos[0] + 2, self.penguin_pos[1])

    def first_obj_coords(self) -> tuple:
        return (self.start_pos[0], self.start_pos[1] + TILE_SIZE // 2)

    def draw(self, screen: pygame.Surface):
        global assests
        for obj in self.objects.values():
            # pygame.draw.polygon(screen, obj.color, obj.points)
            if type(obj) == Hexagon:
                if self.board[obj.y][obj.x] & Tile.FINISH != 0:
                    texture = snow_texture(self.board, obj.x, obj.y)
                    if texture is not None:
                        screen.blit(texture, (obj.points[0][0] - TILE_SIZE // 2, obj.points[0][1]))
                elif self.board[obj.y][obj.x] & Tile.ICE != 0:
                    screen.blit(assests.textures['ICE'], (obj.points[0][0] - TILE_SIZE // 2, obj.points[0][1]))
                    if self.board[obj.y][obj.x] & Tile.PENGUIN != 0:
                        screen.blit(assests.textures['PENGUIN'], (obj.points[0][0] - TILE_SIZE // 2, obj.points[0][1] - TILE_SIZE // 2))
                    
                elif self.board[obj.y][obj.x] & Tile.CRACKED_ICE != 0:
                    if obj.y == 1:
                        texture_pos = 'ICE_' + self.username[obj.x // 2 - 1].upper()
                        if texture_pos not in assests.textures:
                            texture_pos = 'ICE_A'
                        screen.blit(assests.textures[texture_pos], (obj.points[0][0] - TILE_SIZE // 2, obj.points[0][1]))


class Menu(Supervisor):
    def __init__(self, client_socket: socket.socket):
        global assests
        global TILE_SIZE
        self.waiting = False
        self.socket = client_socket
        self.objects = dict()
        self.username = Username()
        self.online_button = Button(
            (self.username.start_pos[0], 2 * TILE_SIZE), 
            [assests.textures['ICON_ONLINE'], assests.textures['ICON_ONLINE_SELECTED']]
            )
        self.local_button = Button(
            (self.username.start_pos[0] + 3 * TILE_SIZE, 2 * TILE_SIZE), 
            [assests.textures['ICON_LOCAL'], assests.textures['ICON_LOCAL_SELECTED']]
            )
        self.local_button.texture_idx = 1
        self.diff_button = Button(
            (self.username.start_pos[0] + 6.5 * TILE_SIZE, 2 * TILE_SIZE), 
            [
                assests.textures['ICON_DIFF_UNSEL'],
                assests.textures['ICON_DIFF_EASY'], 
                assests.textures['ICON_DIFF_NORM'], 
                assests.textures['ICON_DIFF_HARD']
            ]
        )
        self.diff_button.texture_idx = 1
        self.diff_button.texture_start = 1
        self.start_button = Button(
            (self.username.start_pos[0] + 10 * TILE_SIZE, 2 * TILE_SIZE), 
            [
                assests.textures['ICON_START'],
                assests.textures['ICON_START_1'],
                assests.textures['ICON_START_2'],
                assests.textures['ICON_START_3'],
                assests.textures['ICON_START_4'],
                assests.textures['ICON_START_5']
            ]
        )
        self.exit_button = Button(
            (self.username.start_pos[0] + 13 * TILE_SIZE, 2 * TILE_SIZE), 
            [assests.textures['ICON_EXIT']]
        )
        self.objects[self.exit_button.button_id] = self.exit_button
        self.objects[self.start_button.button_id] = self.start_button
        self.objects[self.online_button.button_id] = self.online_button
        self.objects[self.local_button.button_id] = self.local_button
        self.objects[self.diff_button.button_id] = self.diff_button
        self.game_type = GameType.LOCAL
        self.counter = 0
    
    def handle_key(self, key):
        if not self.waiting:
            if key == 8:
                self.username.pop()
            if (key >= 97 and key <= 122) or (key >= 48 and key <= 57):
                self.username.push(chr(key))

    def used_ids(self):
        return self.objects.keys()
    
    def draw(self, screen: pygame.Surface):
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
                        print(f"Seed: {game_state.seed} Turn: {game_state.game_turn}")
                        game_state.seed = int(message.data)
                        self.waiting = False
            except BlockingIOError:
                pass
            except Exception as e:
                print(e)
                self.waiting = False
    
    def handle_click(self, x, y, obj_id):
        if type(self.objects[obj_id]) == Button:
            if obj_id == self.online_button.button_id:
                self.game_type = GameType.ONLINE
                self.local_button.texture_idx = 1 - self.local_button.texture_idx
            elif obj_id == self.local_button.button_id:
                self.game_type = GameType.LOCAL
                self.online_button.texture_idx = 1 - self.online_button.texture_idx
            elif obj_id == self.exit_button.button_id:
                message = Message(Protocol.EXIT, "")
                self.socket.sendall(message.to_bytes())
                pygame.quit()
            elif obj_id == self.start_button.button_id:
                if self.game_type == GameType.ONLINE:
                    message = Message(Protocol.START, f"{self.username.username}")
                    self.socket.sendall(message.to_bytes())
                    self.waiting = True

            self.objects[obj_id].handle_click(x, y, obj_id)
            if obj_id != self.diff_button.button_id:
                if self.online_button.texture_idx == 1:
                    self.diff_button.texture_start = 0
                    self.diff_button.texture_idx = 0
                    self.diff_button.enable = False
                elif self.local_button.texture_idx == 1:
                    self.diff_button.texture_start = 1
                    self.diff_button.enable = True

            if self.online_button.get_state() == 1:
                self.game_type = GameType.ONLINE
            else:
                self.game_type = GameType.LOCAL
    
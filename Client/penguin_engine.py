import pygame
import socket

from Utils.protocol import Protocol, Message

from .gui_params import *
from .game_type import GameType
from .hexagon import Hexagon, Tile
from .hex_utils import create_board, snow_texture, center_board
from .text_field import TextField, TextAlign
from .button import Button

class Turn:
    PENGUIN = 0b0
    WALL = 0b1

class GameStatus:
    RUNNING = 0b0
    PENGUIN_WON = 0b1
    CRACKER_WON = 0b10



class Engine(Supervisor):
    def __init__(
            self, 
            game_type: GameType, 
            seed: int, 
            board_size: tuple = (18, 15), 
            hex_size: int = 64,
            client_socket: socket.socket = None,
            allow_only: Turn = None,
            player_1: str = "Anonymous",
            player_2: str = "Anonymous"
            ):
        global index_buffer
        self.allow_only = allow_only
        self.socket = client_socket
        self.seed = seed
        self.game_type = game_type
        self.board_size = board_size
        self.board = create_board(board_size[1], board_size[0], 0.2, random_seed=seed)
        self.hex_size = hex_size
        self.platform_start = (center_board(board_size, hex_size)[0], 0)
        # self.platform_start = (0, 0)
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
        self.player_1 = None
        self.player_2 = None
        self.player_1 = TextField(
            0, 
            SCREEN_SIZE[1] - 3 * TILE_SIZE, 
            player_1,
            font_color = (25, 129, 157)
            )
        self.player_2 = TextField(
            SCREEN_SIZE[0], 
            SCREEN_SIZE[1] - 3 * TILE_SIZE, 
            player_2, 
            align = TextAlign.RIGHT,
            font_color = (38, 143, 172)
            )
        self.leave_button = Button(
            (
                SCREEN_SIZE[0] // 2 - 1.5 * TILE_SIZE,
                SCREEN_SIZE[1] - 3 * TILE_SIZE
            ),
            [
                assests.textures['ICON_LEFT_PLAYER'],
                assests.textures['ICON_RIGHT_PLAYER'],
                assests.textures['ICON_LEAVE_MATCH'],
                assests.textures['ICON_LOSE_PLAYER'],
                assests.textures['ICON_WIN_PLAYER']
            ]
        )
    

    def handle_click(self, x: int, y: int, obj_id: int):
        if obj_id in self.hex_objects and self.game_status == GameStatus.RUNNING:
            if self.allow_only != None and self.allow_only != self.turn:
                return
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
        def inside_board(x: int, y: int) -> bool:
            return 0 <= x < len(self.board[0]) and 0 <= y < len(self.board)
        penguin_obj = self.hex_objects[self.penguin_id]
        return (
            (inside_board(penguin_obj.x - 2, penguin_obj.y) and 
             self.board[penguin_obj.y][penguin_obj.x - 2] & Tile.ICE != 0)
             or (inside_board(penguin_obj.x + 2, penguin_obj.y) and
                 self.board[penguin_obj.y][penguin_obj.x + 2] & Tile.ICE != 0)
             or (inside_board(penguin_obj.x - 1, penguin_obj.y - 1) and
                 self.board[penguin_obj.y - 1][penguin_obj.x - 1] & Tile.ICE != 0)
             or (inside_board(penguin_obj.x + 1, penguin_obj.y - 1) and
                 self.board[penguin_obj.y - 1][penguin_obj.x + 1] & Tile.ICE != 0)
             or (inside_board(penguin_obj.x - 1, penguin_obj.y + 1) and
                 self.board[penguin_obj.y + 1][penguin_obj.x - 1] & Tile.ICE != 0)
             or (inside_board(penguin_obj.x + 1, penguin_obj.y + 1) and
                 self.board[penguin_obj.y + 1][penguin_obj.x + 1] & Tile.ICE != 0)
        )

    def move_penguin(self, x: int, y: int, obj_id: int):
        penguin_obj = self.hex_objects[self.penguin_id]
        current_obj = self.hex_objects[obj_id]
        if self.board[current_obj.y][current_obj.x] & Tile.ICE == 0:
            return False
        if abs(penguin_obj.x - current_obj.x) > 2 or abs(penguin_obj.y - current_obj.y) > 1:
            return False
        penguin_obj.color, current_obj.color = current_obj.color, penguin_obj.color
        self.board[penguin_obj.y][penguin_obj.x] = Tile.ICE
        self.penguin_id = obj_id
        self.board[current_obj.y][current_obj.x] = Tile.PENGUIN | self.board[current_obj.y][current_obj.x]
        self.turn = Turn.WALL
        self.leave_button.texture_idx = 1
        if self.board[current_obj.y][current_obj.x] & Tile.FINISH != 0:
            self.game_status = GameStatus.PENGUIN_WON
        return True
    
    def place_wall(self, x: int, y: int, obj_id: int):
        current_obj = self.hex_objects[obj_id]
        if (self.board[current_obj.y][current_obj.x] & Tile.PENGUIN != 0 or 
            self.board[current_obj.y][current_obj.x] & Tile.FINISH != 0):
            return False
        self.board[current_obj.y][current_obj.x] = Tile.CRACKED_ICE
        self.hex_objects[obj_id].color = 0xA0A0A0
        self.turn = Turn.PENGUIN
        self.leave_button.texture_idx = 0
        if not self.legal_for_penguin():
            self.game_status = GameStatus.CRACKER_WON
        return True

    def used_ids(self) -> list:
        temp = list(self.hex_objects.keys())
        temp.append(self.leave_button.button_id)
        return temp

    def penguin_texture(self) -> pygame.Surface:
        global assests
        if self.game_status == GameStatus.PENGUIN_WON:
            return assests.textures['PENGUIN']
        elif self.legal_for_penguin():
            return assests.textures['PENGUIN_SCARED']
        return assests.textures['PENGUIN_SAD']

    def draw(self, screen: pygame.Surface):
        global assests
        try:
            data = self.socket.recv(1024, socket.MSG_DONTWAIT)
            if data:
                message = Message.from_bytes(data)
                if message.protocol == Protocol.PENGUIN:
                    x, y = message.data.split()
                    print(x, y)
                    self.move_penguin(int(x), int(y), index_buffer.buffer[int(y)][int(x)])
                elif message.protocol == Protocol.WALL:
                    x, y = message.data.split()
                    self.place_wall(int(x), int(y), index_buffer.buffer[int(y)][int(x)])
        except BlockingIOError:
            pass
        for hexagon in self.hex_objects.values():
            if self.board[hexagon.y][hexagon.x] & Tile.CRACKED_ICE != 0:
                top_left_neigh = self.board[hexagon.y - 1][hexagon.x - 1]
                top_left_neigh = top_left_neigh & Tile.ICE 
                top_right_neigh = self.board[hexagon.y - 1][hexagon.x + 1]
                top_right_neigh = top_right_neigh & Tile.ICE 
                if top_left_neigh and top_right_neigh:
                    screen.blit(assests.textures['HOLE_HALF'], (hexagon.points[0][0] - self.hex_size / 2, hexagon.points[0][1]))
                elif top_left_neigh:
                    screen.blit(assests.textures['HOLE_HALF_LEFT'], (hexagon.points[0][0] - self.hex_size / 2, hexagon.points[0][1]))
                elif top_right_neigh:
                    screen.blit(assests.textures['HOLE_HALF_RIGHT'], (hexagon.points[0][0] - self.hex_size / 2, hexagon.points[0][1]))
                else:
                    screen.blit(assests.textures['HOLE_FULL'], (hexagon.points[0][0] - self.hex_size / 2, hexagon.points[0][1]))
            elif (self.board[hexagon.y][hexagon.x] & Tile.ICE != 0 and 
                  self.board[hexagon.y][hexagon.x] & Tile.FINISH == 0):
                screen.blit(assests.textures['ICE'], (hexagon.points[0][0] - self.hex_size / 2, hexagon.points[0][1]))
            elif self.board[hexagon.y][hexagon.x] & Tile.FINISH != 0:
                texture = snow_texture(self.board, hexagon.x, hexagon.y)
                if texture is not None:
                    screen.blit(texture, (hexagon.points[0][0] - self.hex_size / 2, hexagon.points[0][1]))  
            if hexagon.obj_id == self.penguin_id:
                screen.blit(self.penguin_texture(), (hexagon.points[0][0] - self.hex_size / 2, hexagon.points[0][1] - self.hex_size * 0.25))

        # font = pygame.font.Font(None, 36)
        # if self.game_status & GameStatus.PENGUIN_WON != 0:
        #     text = font.render("PENGUIN WON", True, (255, 255, 255))
        #     screen.blit(text, (0, 0))
        # elif self.game_status & GameStatus.CRACKER_WON != 0:
        #     text = font.render("CRACKER WON", True, (255, 255, 255))
        #     screen.blit(text, (0, 0))
        
        self.player_1.draw(screen)
        self.player_2.draw(screen)

        mouse_pos = pygame.mouse.get_pos()
        
        if self.game_status == GameStatus.RUNNING:
            if index_buffer.buffer[mouse_pos[1]][mouse_pos[0]] == self.leave_button.button_id:
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
        

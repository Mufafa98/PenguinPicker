import random

from Client.bot.utils import Difficulty, a_star, get_neighbors, MED_DIFF_RATIO
from Client.hexagon import Tile


class CrackerBot:
    """
    ### About
    - A class for the cracker bot.
    ### Attributes
    - `__difficulty`: The difficulty level of the bot.
    ### Methods
    - `get_move(board)`: Returns the move of the bot.
    """
    def __init__(self, difficulty: Difficulty):
        """
        ### About
        - Initializes the CrackerBot object.
        ### Parameters
        - `difficulty`: The difficulty level of the bot.
        """
        self.__difficulty = difficulty

    def __easy_move(self, board: list) -> tuple:
        """
        ### About
        - Returns the move of the bot for the easy difficulty level.
        ### Parameters
        - `board`: The game board.
        ### Returns
        - The move of the bot.
        ### Notes
        - The bot places a wall randomly on the board, in the legal moves
        of the penguin.
        """
        penguin_pos = tuple()
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] & Tile.PENGUIN:
                    penguin_pos = (i, j)
                    break
        if board[penguin_pos[0]][penguin_pos[1]] & Tile.FINISH != 0:
            return penguin_pos
        possible_moves_first = [
            (penguin_pos[0] - 1, penguin_pos[1] - 1),
            (penguin_pos[0], penguin_pos[1] - 2),
            (penguin_pos[0] + 1, penguin_pos[1] - 1),
            (penguin_pos[0], penguin_pos[1] + 2),
            (penguin_pos[0] + 1, penguin_pos[1] + 1),
            (penguin_pos[0] - 1, penguin_pos[1] + 1)
        ]
        possible_moves = []
        for move in possible_moves_first:
            if (
                board[move[0]][move[1]] & Tile.ICE != 0
                and board[move[0]][move[1]] & Tile.FINISH == 0
            ):
                possible_moves.append(move)
        return random.choice(possible_moves)

    def __medium_move(self, board: list) -> tuple:
        """
        ### About
        - Returns the move of the bot for the medium difficulty level.
        ### Parameters
        - `board`: The game board.
        ### Returns
        - The move of the bot.
        ### Notes
        - The bot moves randomly between the easy and hard moves.
        """
        global MED_DIFF_RATIO
        if random.random() < MED_DIFF_RATIO:
            return self.__easy_move(board)
        else:
            return self.__hard_move(board)

    def __hard_move(self, board: list) -> tuple:
        """
        ### About
        - Returns the move of the bot for the hard difficulty level.
        ### Parameters
        - `board`: The game board.
        ### Returns
        - The move of the bot.
        ### Notes
        - This approach uses the A* algorithm to find the shortest path to the
        nearest finish tile, and places a wall either on the path if the tile
        has at least one cracked ice neighbor and is in the next move of the
        penguin. Either places a wall on the middle of the path
        """
        penguin_pos = tuple()
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] & Tile.PENGUIN:
                    penguin_pos = (i, j)
                if board[i][j] & Tile.HIGHLIGHTED != 0:
                    board[i][j] = board[i][j] & ~Tile.HIGHLIGHTED

        path = a_star(board, penguin_pos)
        if path is not None and len(path) > 2:

            for move in path:
                neighbors = get_neighbors(move)
                for neighbor in neighbors:
                    if board[neighbor[0]][neighbor[1]] & Tile.CRACKED_ICE != 0:
                        return move

            return path[len(path) // 2]
        else:
            penguin_neighbors = get_neighbors(penguin_pos)
            for neighbor in penguin_neighbors:
                if board[neighbor[0]][neighbor[1]] & Tile.ICE != 0:
                    if board[neighbor[0]][neighbor[1]] & Tile.FINISH == 0:
                        return neighbor

    def get_move(self, board: list) -> tuple:
        """
        ### About
        - Returns the move of the bot.
        ### Parameters
        - `board`: The game board.
        ### Returns
        - The move of the bot.
        """
        if self.__difficulty == Difficulty.EASY:
            return self.__easy_move(board)
        elif self.__difficulty == Difficulty.MEDIUM:
            return self.__medium_move(board)
        elif self.__difficulty == Difficulty.HARD:
            return self.__hard_move(board)
        else:
            raise ValueError("Invalid difficulty level")
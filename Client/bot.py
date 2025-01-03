
from .hexagon import Tile
import random

class Difficulty:
    EASY = 0
    MEDIUM = 1
    HARD = 2

def difficulty(level: int) -> Difficulty:
    if level == 0:
        return Difficulty.EASY
    elif level == 1:
        return Difficulty.MEDIUM
    elif level == 2:
        return Difficulty.HARD
    else:
        raise ValueError("Invalid difficulty level")

def a_star(board: list, start: tuple, end_x: int = None, end_y: int = None) -> list:

    def dist_from_start(node: tuple) -> int:
        return abs(node[0] - start[0])  + abs(node[1] - start[1])
    # TODO Fix heuristic: dist_to_end: it favorises going up and not sideways
    def dist_to_end(node: tuple) -> int:
        if end_x is None and end_y is None:
            distances = []
            for y in range(len(board)):
                for x in range(len(board[y])):
                    if board[y][x] & Tile.FINISH != 0:
                        distances.append(abs(node[0] - y) + abs(node[1] - x) )
            return min(distances)
        elif end_x is None:
            distances = []
            for x in range(len(board[end_y])):
                if board[end_y][x] & Tile.FINISH != 0:
                    distances.append(abs(node[1] - x) + abs(node[0] - end_y))
            return min(distances)
        elif end_y is None:
            distances = []
            for y in range(len(board)):
                if board[y][end_x] & Tile.FINISH != 0:
                    distances.append(abs(node[0] - y) + abs(node[1] - end_x))
            return min(distances)
        return abs(node[0] - end_x) + abs(node[1] - end_y)

    open_list = []
    closed_list = []
    parents = {}

    open_list.append((start, dist_from_start(start), dist_to_end(start)))
    parents[start] = None
    while len(open_list) > 0:
        current = open_list.pop(0)
        closed_list.append(current)
        
        if board[current[0][0]][current[0][1]] & Tile.FINISH != 0:
            path = []
            while current[0] != start:
                path.append(current[0])
                current = (parents[current[0]], 0, 0)
            return path[::-1]
        
        neighbors = [
            (current[0][0] - 1, current[0][1] - 1),
            (current[0][0], current[0][1] - 2),
            (current[0][0] + 1, current[0][1] - 1),
            (current[0][0], current[0][1] + 2),
            (current[0][0] + 1, current[0][1] + 1),
            (current[0][0] - 1, current[0][1] + 1)
        ]

        for neighbor in neighbors:
            neighbor_tuple = (neighbor, dist_from_start(neighbor), dist_to_end(neighbor))
            if neighbor_tuple in closed_list or board[neighbor[0]][neighbor[1]] & Tile.ICE == 0:
                continue
            if neighbor_tuple not in open_list:
                open_list.append(neighbor_tuple)
                open_list.sort(key=lambda x: (x[1] + x[2], x[1]))
                parents[neighbor] = current[0]
            else:
                old_neighbor = open_list[open_list.index(neighbor_tuple)]
                old_distance = old_neighbor[1] + old_neighbor[2]
                new_distance = neighbor_tuple[1] + neighbor_tuple[2]
                if old_distance > new_distance:
                    open_list[open_list.index(neighbor_tuple)] = neighbor_tuple
                    parents[neighbor] = current[0]
                elif old_distance == new_distance:
                    if old_neighbor[1] > neighbor_tuple[1]:
                        open_list[open_list.index(neighbor_tuple)] = neighbor_tuple
                        parents[neighbor] = current[0]
    return path
                
        

class PenguinBot:
    def __init__(self, difficulty: Difficulty):
        self.__difficulty = difficulty
    
    def __easy_move(self, board: list) -> tuple:
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
            # print(board[move[0]][move[1]])
            if (
                board[move[0]][move[1]] & Tile.ICE != 0
            ):
                possible_moves.append(move)
        return random.choice(possible_moves)

    def __medium_move(self, board: list) -> tuple:
        return self.__easy_move(board)

    def __hard_move(self, board: list) -> tuple:
        return self.__easy_move(board)

    def get_move(self, board: list) -> tuple:
        if self.__difficulty == Difficulty.EASY:
            return self.__easy_move(board)
        elif self.__difficulty == Difficulty.MEDIUM:
            return self.__medium_move(board)
        elif self.__difficulty == Difficulty.HARD:
            return self.__hard_move(board)
        else:
            raise ValueError("Invalid difficulty level")
        pass

class CrackerBot:
    def __init__(self, difficulty: Difficulty):
        self.__difficulty = difficulty
        
    def __easy_move(self, board: list) -> tuple:
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
            # print(board[move[0]][move[1]])
            if (
                board[move[0]][move[1]] & Tile.ICE != 0
                and board[move[0]][move[1]] & Tile.FINISH == 0
            ):
                possible_moves.append(move)
        return random.choice(possible_moves)
    
    def __medium_move(self, board: list) -> tuple:
        penguin_pos = tuple()
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] & Tile.PENGUIN:
                    penguin_pos = (i, j)
                if board[i][j] & Tile.HIGHLIGHTED != 0:
                    board[i][j] = board[i][j] & ~Tile.HIGHLIGHTED

        path = a_star(board, penguin_pos)
        
        for move in path:
            board[move[0]][move[1]] = board[move[0]][move[1]] | Tile.HIGHLIGHTED
        return self.__easy_move(board)

    def __hard_move(self, board: list) -> tuple:
        # Implement the bot logic here
        pass

    def get_move(self, board: list) -> tuple:
        if self.__difficulty == Difficulty.EASY:
            return self.__easy_move(board)
        elif self.__difficulty == Difficulty.MEDIUM:
            return self.__medium_move(board)
        elif self.__difficulty == Difficulty.HARD:
            return self.__hard_move(board)
        else:
            raise ValueError("Invalid difficulty level")
        pass


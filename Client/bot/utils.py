"""
### About
- This module contains the bot classes.
### Classes
- `Difficulty`: An enumeration class for the difficulty levels.
- `PenguinBot`: A class for the penguin bot.
- `CrackerBot`: A class for the cracker bot.
### Functions
- `difficulty(level)`: Returns the difficulty level based on the input.
- `get_neighbors(node)`: Returns the neighbors of a node.
"""
from Client.hexagon import Tile


MED_DIFF_RATIO = 0.3
"""
### About
- The medium difficulty is a mix of easy and hard difficulties.
Therefore the ratio of easy to hard is 3:7.
"""


class Difficulty:
    """
    ### About
    - An enumeration class for the difficulty levels.
    """
    EASY = 0
    MEDIUM = 1
    HARD = 2


def difficulty(level: int) -> Difficulty:
    """
    ### About
    - Returns the difficulty level based on the input.
    ### Parameters
    - `level`: The difficulty level.
    ### Returns
    - The difficulty level.
    """
    if level == 0:
        return Difficulty.EASY
    elif level == 1:
        return Difficulty.MEDIUM
    elif level == 2:
        return Difficulty.HARD
    else:
        raise ValueError("Invalid difficulty level")


def get_neighbors(node: tuple) -> list:
    """
    ### About
    - Returns the neighbors of a node.
    ### Parameters
    - `node`: The node.
    ### Returns
    - The neighbors of the node.
    """
    return [
        (node[0] - 1, node[1] - 1),
        (node[0], node[1] - 2),
        (node[0] + 1, node[1] - 1),
        (node[0], node[1] + 2),
        (node[0] + 1, node[1] + 1),
        (node[0] - 1, node[1] + 1)
    ]


def a_star(board: list,
           start: tuple,
           end_x: int = None,
           end_y: int = None) -> list:
    """
    ### About
    - The A* algorithm.
    ### Parameters
    - `board`: The game board.
    - `start`: The start node.
    - `end_x`: The x-coordinate of the end node.
    - `end_y`: The y-coordinate of the end node.
    ### Returns
    - The path.
    ### Notes
    - If the end coords are not provided, the function will search the shortest
    path to the nearest finish tile.
    """
    def dist_from_start(node: tuple) -> int:
        """
        ### About
        - Returns the distance from the start node.
        ### Parameters
        - `node`: The node.
        ### Returns
        - The distance from the start node.
        """
        return abs(node[0] - start[0]) + abs(node[1] - start[1])

    def dist_to_end(node: tuple) -> int:
        """
        ### About
        - Returns the distance to the end node.
        ### Parameters
        - `node`: The node.
        ### Returns
        - The distance to the end node
        """
        def distance(x1: int, x2: int, y1: int, y2: int):
            """
            ### About
            - Returns the distance between two points.
            ### Parameters
            - `x1`: The x-coordinate of the first point.
            - `x2`: The x-coordinate of the second point.
            - `y1`: The y-coordinate of the first point.
            - `y2`: The y-coordinate of the second point.
            ### Returns
            - The distance between the two points.
            """
            return abs(x1 - x2) + abs(y1 - y2) * 2

        if end_x is None and end_y is None:
            distances = []
            for y in range(len(board)):
                for x in range(len(board[y])):
                    if board[y][x] & Tile.FINISH != 0:
                        distances.append(distance(node[1], x, node[0], y))
            return min(distances)
        
        elif end_x is None:
            distances = []
            for x in range(len(board[end_y])):
                if board[end_y][x] & Tile.FINISH != 0:
                    distances.append(distance(node[1], x, node[0], end_y))
            return min(distances)
        
        elif end_y is None:
            distances = []
            for y in range(len(board)):
                if board[y][end_x] & Tile.FINISH != 0:
                    distances.append(distance(node[1], end_x, node[0], y))
            return min(distances)
        
        return distance(node[1], end_x, node[0], end_y)

    # Initialize the open and closed lists
    open_list = []
    closed_list = []
    parents = {}

    open_list.append((start, dist_from_start(start), dist_to_end(start)))
    parents[start] = None

    # Loop until the open list is empty
    while len(open_list) > 0:
        current = open_list.pop(0)
        closed_list.append(current)

        # Check if the current node is the end node
        # If it is, return the path
        if board[current[0][0]][current[0][1]] & Tile.FINISH != 0:
            path = []
            while current[0] != start:
                path.append(current[0])
                current = (parents[current[0]], 0, 0)
            return path[::-1]

        # Get the neighbors of the current node
        # and loop through them
        neighbors = get_neighbors(current[0])
        for neighbor in neighbors:
            neighbor_tuple = (
                neighbor,
                dist_from_start(neighbor),
                dist_to_end(neighbor)
            )
            # If the neighbor is in the closed list skip it
            if (
                neighbor_tuple in closed_list
                or board[neighbor[0]][neighbor[1]] & Tile.ICE == 0
            ):
                continue
            # If the neighbor is not in the open list
            # add it to the open list and set the current node as its parent
            # If it is in the open list, check if the current path is shorter
            # If it is, update the path
            if neighbor_tuple not in open_list:
                open_list.append(neighbor_tuple)
                open_list.sort(key=lambda x: (x[1] + x[2], x[1]))
                parents[neighbor] = current[0]
            else:
                neighbor_idx = open_list.index(neighbor_tuple)
                old_neighbor = open_list[neighbor_idx]

                old_distance = old_neighbor[1] + old_neighbor[2]
                new_distance = neighbor_tuple[1] + neighbor_tuple[2]
                
                if old_distance > new_distance:
                    open_list[neighbor_idx] = neighbor_tuple
                    parents[neighbor] = current[0]
                elif (old_distance == new_distance and 
                      old_neighbor[1] > neighbor_tuple[1]):
                        open_list[neighbor_idx] = neighbor_tuple
                        parents[neighbor] = current[0]
    return None
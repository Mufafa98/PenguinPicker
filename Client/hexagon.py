"""
### About
This module contains the Hexagon class, 
which is used to represent a hexagon on the game board.
"""

from .gui_params import SCREEN_SIZE, index_buffer

HEX_COORDS_COEF = [
    (0.5, 0.0),
    (1, 0.25),
    (1, 0.75),
    (0.5, 1),
    (0, 0.75),
    (0, 0.25),
]
"""
Offsets from the origin(Top left corner) 
for each of the 6 points of the hexagon.
"""

class Tile:
    """
    ### About
    This enum is used to represent the different types of tiles
    ### Note
    - A tile can have multiple types, so the values are bit flags.
    - It should be used using bitwise operations.
    ### Attributes

    | Attribute    | Binary Value |
    |--------------|--------------|
    | EMPTY        | 0b0000000    |
    | PENGUIN      | 0b0000001    |
    | ICE          | 0b0000010    |
    | CRACKED_ICE  | 0b0000100    |
    | FINISH       | 0b0001000    |
    """
    EMPTY = 0b0000000
    PENGUIN = 0b0000001
    ICE = 0b0000010
    CRACKED_ICE = 0b0000100
    FINISH = 0b0001000


class Hexagon:
    """
    ### About
    - This class represents a hexagon on the game board.
    ### Methods
    - `point_in_hexagon(x: int, y: int) -> bool`:
        - This method checks if a point is inside the hexagon.
    - `clone() -> Hexagon`:
        - This method returns a copy of the hexagon.
    ### Attributes
    - `x`: The x coordinate of the hexagon.
    - `y`: The y coordinate of the hexagon.
    - `size`: The size of the hexagon.
    - `color`: The color of the hexagon.
    - `obj_id`: The id of the object.
    - `points`: The 6 points that define the hexagon.
    """
    def __init__(
            self, platform_start: tuple,
            x: int, y: int, size: int,
            obj_id: int, color: int = 0x000000):
        """
        ### About
        - This method initializes the hexagon.
        ### Parameters
        - `platform_start`: The starting position of the platform.
        - `x`: The x coordinate of the hexagon in the board.
        - `y`: The y coordinate of the hexagon.

        """
        global index_buffer
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.obj_id = obj_id
        screen_x = platform_start[0] + (x * 0.5) * size
        screen_y = platform_start[1] + (y * 0.75) * size
        self.points = [
            [
                screen_x + self.size * coef[0],
                screen_y + self.size * coef[1]
            ] for coef in HEX_COORDS_COEF
        ]
        x_start = int(screen_x)
        y_start = int(screen_y)
        x_end = int(x_start + size)
        y_end = int(y_start + size)
        for temp_y in range(y_start, y_end):
            for temp_x in range(x_start, x_end):
                if self.point_in_hexagon(temp_x, temp_y):
                    # Avoid drawing outside the screen in order
                    # to avoid index out of bounds error
                    if temp_x < 0 or temp_x >= SCREEN_SIZE[0]:
                        continue
                    if temp_y < 0 or temp_y >= SCREEN_SIZE[1]:
                        continue
                    index_buffer.buffer[temp_y][temp_x] = (self.obj_id)

    def point_in_hexagon(self, x: int, y: int) -> bool:
        """
        ### About
        - This method checks if a point is inside the hexagon.
        - It is used mainly for the Index Buffer.
        ### Parameters
        - `x`: The x coordinate of the point.
        - `y`: The y coordinate of the point.
        ### Returns
        - `bool`: True if the point is inside the hexagon, False otherwise.
        ### Note
        - This method uses the baricentric coordinates method
        - Basically, if the area of the 3 triangles formed by the point
        and the 3 points of the upper respectively lower triangle is equal
        to the area of the main triangle
        """
        def triangle_area(A: tuple, B: tuple, C: tuple):
            """
            ### About
            - This method calculates the area of a triangle.
            ### Parameters
            - `A`: The first point of the triangle.
            - `B`: The second point of the triangle.
            - `C`: The third point of the triangle.
            ### Returns
            - `float`: The area of the triangle.
            """
            return abs(
                (
                    A[0] * (B[1] - C[1]) +
                    B[0] * (C[1] - A[1]) +
                    C[0] * (A[1] - B[1])
                ) / 2.0
            )
        if y <= self.points[1][1]:
            a, b, c = self.points[0], self.points[1], self.points[5]
            main_area = triangle_area(a, b, c)
            area1 = triangle_area((x, y), a, b)
            area2 = triangle_area((x, y), b, c)
            area3 = triangle_area((x, y), c, a)
            return main_area == area1 + area2 + area3
        elif y >= self.points[2][1]:
            a, b, c = self.points[2], self.points[3], self.points[4]
            main_area = triangle_area(a, b, c)
            area1 = triangle_area((x, y), a, b)
            area2 = triangle_area((x, y), b, c)
            area3 = triangle_area((x, y), c, a)
            return main_area == area1 + area2 + area3
        return True

    def clone(self):
        """
        ### About
        - This method returns a copy of the hexagon.
        ### Returns
        - `Hexagon`: A copy of the hexagon.
        """
        return Hexagon(self.x, self.y, self.size, self.obj_id, self.color)

    def __str__(self):
        return f"Hexagon({self.x}, {self.y}, {self.size}, {self.obj_id})\n"

    def __repr__(self):
        return self.__str__()

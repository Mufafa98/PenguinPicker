BACKGROUND_COLOR = (123, 123, 123)
SCREEN_SIZE = (1000, 800)
FPS = 60

# INDEX BUFFER
# Credit: Alex Mitreanu
index_buffer = [
    [[] for _ in range(0, SCREEN_SIZE[0])] for _ in range(0, SCREEN_SIZE[1])
]

OBJECT_ID = 0

class Supervisor:
    def handle_click(self, x: int, y: int, obj_id: int):
        raise NotImplementedError("Method not implemented")
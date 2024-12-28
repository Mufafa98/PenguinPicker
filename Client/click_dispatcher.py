from .gui_params import index_buffer, Supervisor

class AlreadyRegisteredError(Exception):
    def __init__(self, message):
        super().__init__(message)

class ClickDispatcher:
    def __init__(self):
        self.object_mapping = dict()

    def restart(self):
        self.object_mapping = dict()

    def register_object(self, obj_id: int, object_supervisor: Supervisor):
        if obj_id in self.object_mapping:
            raise AlreadyRegisteredError(f"Object with id {obj_id} already registered")
        self.object_mapping[obj_id] = object_supervisor
    
    def register_objects(self, object_ids: list, object_supervisor: Supervisor):
        for obj_id in object_ids:
            self.register_object(obj_id, object_supervisor)
    
    def peek_object_mapping(self):
        return self.object_mapping
    
    def dispatch_click(self, x: int, y: int):
        global index_buffer
        obj_id = index_buffer.buffer[y][x]
        if type(obj_id) is not int:
            print(f"No object found at ({x}, {y})")
        elif obj_id in self.object_mapping:
            self.object_mapping[obj_id].handle_click(x, y, obj_id)
            
        
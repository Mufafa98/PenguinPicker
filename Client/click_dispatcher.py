"""
### About
- This class is responsible for dispatching clicks to the correct supervisor.
"""
from .gui_params import index_buffer, Supervisor


class AlreadyRegisteredError(Exception):
    """
    ### About
    - This exception is raised when an object is already registered.
    """
    def __init__(self, message):
        super().__init__(message)


class ClickDispatcher:
    """
    ### About
    - This class is responsible for dispatching clicks to the correct
    supervisor.
    ### Methods
    - `restart`: Resets the object mapping.
    - `register_object`: Registers an object with the dispatcher.
    - `register_objects`: Registers multiple objects with the dispatcher.
    - `peek_object_mapping`: Returns the object mapping.
    - `dispatch_click`: Dispatches a click to the correct supervisor.
    ### Attributes
    - `object_mapping`: A dictionary that maps object ids to supervisors.
    """
    def __init__(self):
        """
        ### About
        - Initializes the object mapping.
        """
        self.object_mapping = dict()

    def restart(self):
        """
        ### About
        - Resets the object mapping.
        """
        self.object_mapping = dict()

    def register_object(self, obj_id: int, object_supervisor: Supervisor):
        """
        ### About
        - Registers an object with the dispatcher.
        ### Parameters
        - `obj_id`: The id of the object.
        - `object_supervisor`: The supervisor of the object.
        ### Exceptions
        - `AlreadyRegisteredError`: If the object is already registered.
        """
        if obj_id in self.object_mapping:
            raise AlreadyRegisteredError(
                f"Object with id {obj_id} already registered"
            )
        self.object_mapping[obj_id] = object_supervisor

    def register_objects(
        self,
        object_ids: list,
        object_supervisor: Supervisor
    ):
        """
        ### About
        - Registers multiple objects with the dispatcher.
        ### Parameters
        - `object_ids`: The ids of the objects.
        - `object_supervisor`: The supervisor of the objects.
        ### Exceptions
        - `AlreadyRegisteredError`: If an object is already registered.
        """
        for obj_id in object_ids:
            self.register_object(obj_id, object_supervisor)

    def peek_object_mapping(self):
        """
        ### About
        - Returns the object mapping.
        """
        return self.object_mapping

    def dispatch_click(self, x: int, y: int):
        """
        ### About
        - Dispatches a click to the correct supervisor.
        ### Parameters
        - `x`: The x coordinate of the click.
        - `y`: The y coordinate of the click.
        """
        global index_buffer
        obj_id = index_buffer.buffer[y][x]
        if type(obj_id) is not int:
            print(f"No object found at ({x}, {y})")
        elif obj_id in self.object_mapping:
            self.object_mapping[obj_id].handle_click(x, y, obj_id)

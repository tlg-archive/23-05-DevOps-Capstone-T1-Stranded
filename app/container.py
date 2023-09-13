#imports
from app.entity import Entity


class Container(Entity):
    def __init__(self,
                 obj_id: str,
                 name: str,
                 description: str,
                 state: bool,
                 inventory: list[tuple[str, int]]
                 ):
        super().__init__(obj_id, name, description, state)
        if not inventory:
            inventory = []
        self.inventory = inventory

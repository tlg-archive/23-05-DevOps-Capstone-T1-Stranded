#imports
from app.entity import Entity


class Container(Entity):
    def __init__(self,
                 obj_id: str,
                 name: str,
                 description: str,
                 state: bool,
                 inventory: list[dict[str, int or str]]
                 ):
        super().__init__(obj_id, name, description, state)
        self.inventory = []
        if inventory:
            for item in inventory:
                self.inventory.append((item['kind'], item['obj_id']))

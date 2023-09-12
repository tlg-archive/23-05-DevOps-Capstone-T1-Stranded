
from app.entity import Entity

class Player(Entity):
    def __init__(self,
                 obj_id: int,
                 name: str,
                 description: str,
                 state: str,
                 inventory: list[tuple[str, int]]
                 ):
        super().__init__(obj_id, name, description, state)
        if not inventory:
            inventory = []
        self.inventory = inventory
        
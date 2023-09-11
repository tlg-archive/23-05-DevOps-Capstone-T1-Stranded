
from app.entity import entity

class player(entity): 
    def __init__(self, id: int, name: str, description: str, state: str, inventory: list[tuple[str, int]]):
        super().__init__(id, name, description, state)
        if not inventory:
            inventory = []
        self.inventory = inventory
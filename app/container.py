#imports
from app.interactable import interactable


class container(interactable):
    def __init__(self, id: str, name: str, description: str, state: bool, inventory: list[tuple[str, int]]):
        super().__init__(id, name, description, state)
        if not inventory:
            inventory = []
        self.inventory = inventory
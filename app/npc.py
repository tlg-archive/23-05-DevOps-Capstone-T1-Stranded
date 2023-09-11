from app.interactable import interactable


class npc(interactable): 
    def __init__(self, id: str, name: str, description: str, state: bool, dialogue: str, inventory: list[tuple[str, int]]):
        super().__init__(id, name, description, state)
        self.dialogue = dialogue
        if not inventory:
            inventory = []
        self.inventory = inventory
        
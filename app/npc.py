from app.interactable import Interactable


class Npc(Interactable):
    def __init__(self,
                 obj_id: str,
                 name: str,
                 description: str,
                 state: bool,
                 dialogue: str,
                 inventory: list[tuple[str, int]]
                 ):
        super().__init__(obj_id, name, description, state)
        self.dialogue = dialogue
        if not inventory:
            inventory = []
        self.inventory = inventory
        
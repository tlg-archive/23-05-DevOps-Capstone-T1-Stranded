from app.container import Container
import random


class Npc(Container):
    def __init__(self,
                 obj_id: str,
                 name: str,
                 description: str,
                 state: bool,
                 inventory: list[dict[str, str or int]],
                 dialogue: list[str]
                 ):
        super().__init__(obj_id, name, description, state, inventory)
        if not dialogue:
            dialogue = []
        self._dialogue = dialogue
        
    @property
    def dialogue(self) -> str:
        return random.choice(self._dialogue)
        
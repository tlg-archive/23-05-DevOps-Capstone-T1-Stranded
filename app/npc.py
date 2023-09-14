from app.container import Container
import random


class Npc(Container):
    def __init__(self,
                 obj_id: str,
                 name: str,
                 description: str,
                 state: bool,
                 inventory: list[tuple[str, int]],
                 dialogue: list[str]
                 ):
        super().__init__(obj_id, name, description, state, inventory)
        self._dialogue = dialogue
        
    @property
    def dialogue(self) -> str:
        return random.choice(self._dialogue)
        
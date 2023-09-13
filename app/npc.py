from app.container import Container


class Npc(Container):
    def __init__(self,
                 obj_id: str,
                 name: str,
                 description: str,
                 state: bool,
                 inventory: list[tuple[str, int]],
                 dialogue: str
                 ):
        super().__init__(obj_id, name, description, state, inventory)
        self.dialogue = dialogue
        
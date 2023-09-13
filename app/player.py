
from app.container import Container


class Player(Container):
    def __init__(self,
                 obj_id: int,
                 name: str,
                 description: str,
                 state: str,
                 inventory: list[tuple[str, int]]
                 ):
        super().__init__(obj_id, name, description, state, inventory)
        
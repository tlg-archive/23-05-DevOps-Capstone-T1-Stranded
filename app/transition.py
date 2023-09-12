from app.interactable import Interactable


class Transition(Interactable):
    def __init__(self,
                 obj_id: str,
                 name: str,
                 description: str,
                 state: bool,
                 target: tuple[str, int]
                 ):
        super().__init__(obj_id, name, description, state)
        self.target = target

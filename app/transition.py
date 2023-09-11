from app.interactable import interactable


class Transition(interactable):
<<<<<<< HEAD
    def __init__(self, id: str, state: bool, target: tuple[str, int]):
        super().__init__(id, state)
=======
    def __init__(self, id: str, name: str, description: str, state: bool, target: tuple[str, int]):
        super().__init__(id, name, description, state)
>>>>>>> 512d614a96574da0d408736bc7457b14753eeec6
        self.target = target

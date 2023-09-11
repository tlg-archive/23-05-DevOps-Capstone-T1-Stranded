from app.interactable import interactable


class Transition(interactable):
    def __init__(self, id: str, name: str, description: str, state: bool, target: tuple[str, int]):
        super().__init__(id, name, description, state)
        self.target = target

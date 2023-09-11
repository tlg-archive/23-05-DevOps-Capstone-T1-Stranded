from app.interactable import interactable


class Transition(interactable):
    def __init__(self, id: str, state: bool, target: tuple[str, int]):
        super().__init__(id, state)
        self.target = target

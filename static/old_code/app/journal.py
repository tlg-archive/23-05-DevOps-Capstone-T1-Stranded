from app.game_object import GameObject
import random


class Journal(GameObject):
    def __init__(self, obj_id: str, name: str, description: str, dialogue: list[str], story: str  ):
        super().__init__(obj_id, name, description)
        self.story = story
        self._dialogue = dialogue

    @property
    def dialogue(self) -> str:
        return random.choice(self._dialogue)

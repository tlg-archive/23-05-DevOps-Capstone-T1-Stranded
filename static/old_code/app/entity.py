#imports
from app.game_object import GameObject

class Entity(GameObject):
    def __init__(self, obj_id: str, name: str, description: str, state: str):
        super().__init__(obj_id, name, description)
        self.state = state

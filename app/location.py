#imports
from app.game_object import GameObject


class Location(GameObject):
    def __init__(self, obj_id: str, name: str, description: str, entities: list[tuple[str, int]]):
        super().__init__(obj_id, name, description)
        self.entities = entities
        
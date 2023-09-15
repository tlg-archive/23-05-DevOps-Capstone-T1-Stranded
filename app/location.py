#imports
from app.game_object import GameObject


class Location(GameObject):
    def __init__(self, obj_id: str, name: str, description: str, entities: list[dict[str, int or str]]):
        super().__init__(obj_id, name, description)
        self.entities = []
        if entities:
            for entity in entities:
                self.entities.append((entity['kind'], entity['obj_id']))
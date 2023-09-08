#imports
from app.game_object import game_object


class location(game_object): 
    def __init__(self, id: str, name: str, description: str, entities: list[tuple[str, int]]):
        super().__init__(id, name, description)
        self.entities = entities
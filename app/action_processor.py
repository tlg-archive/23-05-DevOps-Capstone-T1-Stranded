#imports

from app.game_object import game_object
from app.location import location


class Action_Processor:
    def __init__(self):
        pass

    def look(self, search_location: location, game_objects: dict[str, game_object], *args) -> str:
        if args:
            looking_for = args[0]
            entities = [game_objects[f'{kind}s'][id] for kind, id in search_location.entities if game_objects[f'{kind}s'][id].name == looking_for]
            if entities:
                return entities[0].description
            else:
                return f"You can't seem to find any {looking_for}s here."

    def process(self, command: str) -> callable:
        if command == 'look':
            return self.look


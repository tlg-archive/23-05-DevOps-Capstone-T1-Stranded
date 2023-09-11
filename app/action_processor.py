#imports

from app.game_object import game_object
from app.location import location
from app.transition import Transition
from app.container import container as Container


class Action_Processor:
    def __init__(self):
        pass

    def look(self, search_location: location, game_objects: dict[str, game_object], *args) -> str:
        if args:
            looking_for = args[0]
            entities = [game_objects[f'{kind}s'][id] for kind, id in search_location.entities if game_objects[f'{kind}s'][id].name == looking_for]
            if entities:
                if isinstance(entities[0], Container):
                    container = entities[0]
                    text = f'{container.description}\n\tinventory:'
                    for kind, id in container.inventory:
                       text = f'{text}\n\t\t{game_objects[f"{kind}s"][id].name}' 
                    return text

                return entities[0].description
            else:
                return f"You can't seem to find any {looking_for}s here."

    def move(self, search_location: location, game_objects: dict[str, game_object], *args) -> str:
        if args:
            moving = args[0]
            transitions = [game_objects[f'{kind}s'][id] for kind, id in search_location.entities if game_objects[f'{kind}s'][id].name == moving]
            if transitions:
                return transitions[0].target
            else: 
                return f"You can't move to the {transitions}."
    
    def take(self, search_location: location, game_objects: dict[str, game_object], *args) -> str:
        if args:
            if len(args) == 1:
                looking_for = args[0]
                items = [(kind, id) for kind, id in search_location.entities if game_objects[f'{kind}s'][id].name == looking_for]
                player = game_objects['players'][0]
                if items:
                    item = items[0]
                    player.inventory.append(search_location.entities.pop(search_location.entities.index(item)))
                    kind, id = item
                    return f"You pickup the {game_objects[f'{kind}s'][id].name}."
                else:
                    return f"You can't seem to find a {looking_for} here." 
            elif len(args) == 2:
                looking_for = args[0]
                container = args[1]
                containers = [game_objects[f'{kind}s'][id] for kind, id in search_location.entities if game_objects[f'{kind}s'][id].name == container]
                player = game_objects['players'][0]
                if containers:
                    container = containers[0]
                    items = [(kind, id) for kind, id in container.inventory if game_objects[f'{kind}s'][id].name == looking_for]
                    if items:
                        item = items[0]
                        player.inventory.append(container.inventory.pop(container.inventory.index(item)))
                        kind, id = item
                        return f"You take the {game_objects[f'{kind}s'][id].name} from inside the {container.name}."

                    return f"You there is not a {looking_for} in the {container.name}"
                else:
                    return f"You can't seem to find a {container} here."

    def process(self, command: str) -> callable:
        if command == 'look':
            return self.look
        if command == "move":
            return self.move
        if command == 'take':
            return self.take
    

#imports

from app.game_object import GameObject
from app.intractable import Intractable
from app.location import Location
from app.container import Container
from app.npc import Npc
from app.transition import Transition
from app.player import Player


class ActionProcessor:
    def __init__(self):
        pass

    def look(self, search_location: Location, game_objects: dict[str, GameObject], *args) -> str:
        if args:
            looking_for = args[0]
            entities = [
                game_objects[f'{kind}s'][obj_id]
                for kind, obj_id
                in search_location.entities
                if game_objects[f'{kind}s'][obj_id].name == looking_for
            ]
            if entities:
                if isinstance(entities[0], Container):
                    container = entities[0]
                    text = f'{container.description}\n\tinventory:'
                    for kind, obj_id in container.inventory:
                        text = f'{text}\n\t\t{game_objects[f"{kind}s"][obj_id].name}'
                    return text
                return entities[0].description
            return f"You can't seem to find any {looking_for}s here, try using the help command."

    def move(self, search_location: Location, game_objects: dict[str, GameObject], *args) -> str or callable:
        if args:
            moving = args[0]
            transitions: list[Transition] = [
                game_objects[f'{kind}s'][obj_id]
                for kind, obj_id
                in search_location.entities
                if game_objects[f'{kind}s'][obj_id].name == moving
                and isinstance(game_objects[f'{kind}s'][obj_id], Transition)
            ]
            if transitions:
                transition: Transition = transitions[0] 
                if not transition.blocked:
                    return transition.target
                return f"You can't go that way because the {transition.name} is {transition.state}"
            return f"You can't move to the {transitions}, try using the help command."

    def wrong(self, *args):
        return "command not found please use the help command to see valid commands and examples"

    def take(self, search_location: Location, game_objects: dict[str, GameObject], *args) -> str:
        if args:
            if len(args) == 1:
                looking_for = args[0]
                items = [
                    (kind, obj_id)
                    for kind, obj_id
                    in search_location.entities
                    if game_objects[f'{kind}s'][obj_id].name == looking_for
                    and not isinstance(game_objects[f'{kind}s'][obj_id], Transition)
                    and not isinstance(game_objects[f'{kind}s'][obj_id], Npc)
                ]
                player = game_objects['players'][0]
                if items:
                    item = items[0]
                    player.inventory.append(
                        search_location.entities.pop(search_location.entities.index(item))
                    )
                    kind, obj_id = item
                    return f"You pickup the {game_objects[f'{kind}s'][obj_id].name}."
                return f"You can't pick up the {looking_for}."
            if len(args) == 2:
                looking_for = args[0]
                container = args[1]
                containers = [
                    game_objects[f'{kind}s'][obj_id]
                    for kind, obj_id
                    in search_location.entities
                    if game_objects[f'{kind}s'][obj_id].name == container
                ]
                player = game_objects['players'][0]
                if containers:
                    container = containers[0]
                    if not isinstance(container, Container):
                        return f"{container.name.capitalize()} is not a container."
                    items = [
                        (kind, obj_id)
                        for kind, obj_id
                        in container.inventory
                        if game_objects[f'{kind}s'][obj_id].name == looking_for
                        and not isinstance(game_objects[f'{kind}s'][obj_id], Location)
                        and not isinstance(game_objects[f'{kind}s'][obj_id], Npc)
                    ]
                    if items:
                        item = items[0]
                        player.inventory.append(
                            container.inventory.pop(container.inventory.index(item))
                        )
                        kind, obj_id = item
                        return f"You take the {game_objects[f'{kind}s'][obj_id].name} from inside the {container.name}."

                    return f"You can't take the {looking_for} from the {container.name}"
                return f"You can't seem to find a {container} here."

    def drop(self, search_location: Location, game_objects: dict[str, GameObject], *args) -> str:
        if args:
            if len(args) == 1:
                looking_for = args[0]
                player = game_objects['players'][0]
                items = [
                    (kind, obj_id)
                    for kind, obj_id
                    in player.inventory
                    if game_objects[f'{kind}s'][obj_id].name == looking_for
                ]
                if items:
                    item = items[0]
                    search_location.entities.append(
                        player.inventory.pop(player.inventory.index(item))
                    )
                    kind, obj_id = item
                    return f"You drop the {game_objects[f'{kind}s'][obj_id].name} on the ground."
                return f"You don't have a {looking_for}."
            if len(args) == 2:
                looking_for = args[0]
                container = args[1]
                containers = [
                                game_objects[f'{kind}s'][obj_id]
                                for kind, obj_id
                                in search_location.entities
                                if game_objects[f'{kind}s'][obj_id].name == container
                             ]
                player = game_objects['players'][0]
                if containers:
                    container = containers[0]
                    if not isinstance(container, Container):
                        return f"{container.name.capitalize()} is not a container."
                    items = [
                                (kind, obj_id)
                                for kind, obj_id
                                in player.inventory
                                if game_objects[f'{kind}s'][obj_id].name == looking_for
                            ]
                    if items:
                        item = items[0]
                        container.inventory.append(
                            player.inventory.pop(player.inventory.index(item))
                        )
                        kind, obj_id = item
                        return f"You put the {game_objects[f'{kind}s'][obj_id].name} in the {container.name}."
                    return f"You don't have a {looking_for}."
                return f"You can't seem to find a {container} here."

    def inventory(self, search_location: Location, game_objects: dict[str, GameObject], *args):
        player: Player = game_objects['players'][0]
        if len(args) == 1:
            looking_for = args[0]
            player = game_objects['players'][0]
            items = [
                (kind, obj_id)
                for kind, obj_id
                in player.inventory
                if game_objects[f'{kind}s'][obj_id].name == looking_for
            ]
            if items:
                item = items[0]
                kind, obj_id = item
                item_obj = game_objects[f'{kind}s'][obj_id]
                text = f"{item_obj.name}: {item_obj.description}"
                if kind == 'container':
                    items = [
                        (kind, obj_id)
                        for kind, obj_id
                        in item_obj.inventory
                    ]
                    if items:
                        text = f'{text}\n\tinventory:'
                        for item in items:
                            kind, obj_id = item
                            text = f"{text}\n\t\t{game_objects[f'{kind}s'][obj_id].name}"
                return text
            return f"You don't have a {looking_for}."
        if len(args) == 2:
            looking_for = args[0]
            player = game_objects['players'][0]
            containers = [
                (kind, obj_id)
                for kind, obj_id
                in player.inventory
                if game_objects[f'{kind}s'][obj_id].name == args[1]
                and isinstance(game_objects[f'{kind}s'][obj_id], Container)
            ]
            if containers:
                container = containers[0]
                items = [
                    (kind, obj_id)
                    for kind, obj_id
                    in container.inventory
                    if game_objects[f'{kind}s'][obj_id].name == looking_for
                ]
                if items:
                    item = items[0]
                    kind, obj_id = item
                    return f"{game_objects[f'{kind}s'][obj_id].name}: {game_objects[f'{kind}s'][obj_id].description}"
            return f"You don't have a {looking_for}."

        items = [
            (kind, obj_id)
            for kind, obj_id
            in player.inventory
        ]
        if items:
            text = '\ninventory:'
            for item in items:
                kind, obj_id = item
                text = f"{text}\n\t{game_objects[f'{kind}s'][obj_id].name}"
            return text
        return "Your inventory is empty."

    def use(self, search_location: Location, game_objects: dict[str, GameObject], *args) -> str:
        if len(args) == 1:
            target = args[0]
            intractables: list[Intractable] = [
                game_objects[f'{kind}s'][obj_id]
                for kind, obj_id
                in search_location.entities
                if game_objects[f'{kind}s'][obj_id].name == target
                and isinstance(game_objects[f'{kind}s'][obj_id], Intractable)
            ]
            if intractables:
                intractable: Intractable = intractables[0]
                return intractable.cycle()
            return f"You can't use the {target} right now."
        if len(args) == 2:
            key_name = args[0]
            target_name = args[1]

            keys = [
                (kind, obj_id)
                for kind, obj_id
                in search_location.entities
                if game_objects[f'{kind}s'][obj_id].name == key_name
            ]
            if not keys:
                player = game_objects['players'][0]
                keys = [
                    (kind, obj_id)
                    for kind, obj_id
                    in player.inventory
                    if game_objects[f'{kind}s'][obj_id].name == key_name
                ]
            if not keys:
                return f"You don't have a {key_name} and there isn't one near you either."
            targets = [
                game_objects[f'{kind}s'][obj_id] 
                for kind, obj_id
                in search_location.entities
                if game_objects[f'{kind}s'][obj_id].name == target_name
                and isinstance(game_objects[f'{kind}s'][obj_id], Intractable)
            ]
            if targets:
                key = keys[0]
                target: Intractable = targets[0]
                return target.unlock(key, key_name)
            return f"There isn't a {target_name} here."

        if len(args) < 1:
            return 'Invalid usage of command [use]. requires at least one argument. please use the help command for more information'

    def process(self, command: str) -> callable:
        if command == 'look':
            return self.look
        if command == "move":
            return self.move
        if command == 'take':
            return self.take
        if command == 'drop':
            return self.drop
        if command == 'inventory':
            return self.inventory
        if command == 'use':
            return self.use
        return self.wrong

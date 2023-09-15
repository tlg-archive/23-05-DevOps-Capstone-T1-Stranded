#! /usr/bin/env python3
# James L. Rogers | github.com/DarkWinged

#imports
import curses
import os
import platform
import json
import pygame
from app.event import Event
from app.npc import Npc
from app.parser import Parser
from app.location import Location
from app.item import Item
from app.game_object import GameObject
from app.action_processor import ActionProcessor
from app.transition import Transition
from app.player import Player
from app.container import Container
from app.journal import Journal

def load_data() -> dict[str, any]:
    data = {}
    with open(
        f"{'/'.join(os.path.abspath(__file__).split('/')[:-1])}/data/title.txt", 
        'r',
        encoding="utf-8"
        ) as title_file:
        data['title'] = title_file.readlines()

    with open(
        f"{'/'.join(os.path.abspath(__file__).split('/')[:-1])}/data/description.txt",
        "r",
        encoding="utf-8"
        ) as plot:
        plot = plot.read().splitlines()
    plot_splice = []
    splice_len = 50
    for i in range(0, len(plot), splice_len):
        plot_splice.append(plot[i:i+splice_len])
    data['opening'] = plot_splice

    with open(
              f"{'/'.join(os.path.abspath(__file__).split('/')[:-1])}/data/help.txt",
              "r",
              encoding="utf-8"
              ) as help_file:
        data['help'] = help_file.read()
    
    with open(
              f"{'/'.join(os.path.abspath(__file__).split('/')[:-1])}/data/map.txt",
              "r",
              encoding="utf-8"
              ) as map_file:
        data['map'] = map_file.read()

    object_types = ['locations', 'items', 'transitions', 'players', 'containers', 'npcs', "journals", 'events']

    for object_type in object_types:
        with open(
            f"{'/'.join(os.path.abspath(__file__).split('/')[:-1])}/data/{object_type}.json",
            "r",
            encoding="utf-8"
            ) as loading:
            data[object_type] = json.load(loading)

    return data

def load_game_objects(data: dict[str, any]):
    objects = {}

    objects['npcs'] = {}
    for npc in data['npcs']:
        items = []
        if "inventory" in npc.keys():
            for item in npc['inventory']:
                items.append((item['kind'], item['obj_id']))
        if "dialogue" in npc.keys():
            for npc in data["npcs"]: 
                npc_obj = Npc(npc['obj_id'],
                            npc['name'],
                            npc['description'],
                            npc['state'],
                            items,
                            npc['dialogue']
                            )
                objects['npcs'][npc_obj.obj_id] = npc_obj

    objects['locations'] = {}
    for location in data['locations']:
        entities = []
        if 'entities' in location.keys():
            for entity in location['entities']:
                entities.append((entity['kind'], entity['obj_id']))
        location_obj = Location(location['obj_id'],
                                location['name'],
                                location['description'],
                                entities
                                )
        objects['locations'][location_obj.obj_id] = location_obj
    
    objects['journals'] = {}
    for journal in data['journals']:
        journal_obj = Journal(journal['obj_id'],
                        journal['name'],
                        journal['description'],
                        journal['dialogue'],
                        journal['story']
                        )
        objects['journals'][journal_obj.obj_id] = journal_obj

    objects['items'] = {}
    for item in data['items']:

        item_obj = Item(item['obj_id'], item['name'], item['description'], None)

        objects['items'][item_obj.obj_id] = item_obj
    objects['transitions'] = {}
    for transition in data['transitions']:
        target = (transition['target']['kind'], transition['target']['obj_id'])
        key_info = transition.get('key_info', {})
        if key_info:
            key_info['key'] = (key_info['key']['kind'], key_info['key']['obj_id'])
        transition_obj = Transition(transition['obj_id'],
                                    transition['name'],
                                    transition['description'],
                                    transition['state'],
                                    transition['state_descriptions'],
                                    transition['state_transitions'],
                                    transition['state_list'],
                                    key_info,
                                    target,
                                    transition['blocking_states']
                                    )
        objects['transitions'][transition_obj.obj_id] = transition_obj

    objects['players'] = {}
    for player in data['players']:
        inventory = []
        if player.get('inventory', []):
            for item in player['inventory']:
                inventory.append((item['kind'], item['obj_id']))
        player_obj = Player(player['obj_id'],
                            player['name'],
                            player['description'],
                            player['state'],
                            inventory
                            )
        objects['players'][player_obj.obj_id] = player_obj

    objects['containers'] = {}
    for container in data['containers']:
        inventory = []
        if container.get('inventory', []):
            for item in container['inventory']:
                inventory.append((item['kind'], item['obj_id']))
        container_obj = Container(container['obj_id'],
                                  container['name'],
                                  container['description'],
                                  container['state'],
                                  inventory
                                  )
        objects['containers'][container_obj.obj_id] = container_obj

    objects['events'] = {}
    for event_data in data['events']:
        # Convert event_data to Event object
        event = Event(
            event_data['obj_id'],
            event_data['name'],
            event_data['description'],
            event_data['state'],
            event_data['triggers'],
            event_data['affected_objects'],
            event_data['change']
        )
        objects['events'][event.obj_id] = event

    return objects

def resize_terminal(desired_height: int, desired_width: int):
    # Resize the terminal window
    system_platform = platform.system()
    cols, rows = desired_width*8, desired_height*10
    if system_platform == "Darwin":  # macOS
        os.system(f"osascript -e 'tell application \"Terminal\" to set size of front window to {{ {cols}, {rows} }}'")
    elif system_platform == "Linux" and "X11" in os.environ.get("DISPLAY", ""):  # Linux with X11
        os.system(f"resize -s {rows} {cols}")
    elif system_platform == "Windows":  # Windows
        os.system(f"mode con cols={cols} lines={rows}")

    curses.resizeterm(desired_height, desired_width)

def title(stdscr, data: list[str]):
    height, width = stdscr.getmaxyx()

    for index, line in enumerate(data):
        stdscr.addstr(index, (width - len(line)) // 2, f'{line}')

    message = "Type START to play"
    stdscr.addstr(10, (width - len(message)) // 2, message)

def opening(stdscr, data: list[list[str]]):
    height, width = stdscr.getmaxyx()

    for index, string_list in enumerate(data):
        for string_index, string in enumerate(string_list):
            stdscr.addstr(5 + index + string_index, (width - len(string)) // 2, string)

def help_func(stdscr, data: str):
    stdscr.addstr(1,0, f'{data}')

def map_func(stdscr, data: str):
    stdscr.addstr(1,0, f'{data}')

def generate_location_text(location: Location, game_objs: dict[str, GameObject]) -> str:
    text = location.description
    if location.entities:
        text = f'{text}\nAround you, you can see:'
        for kind, obj_id in location.entities:
            entity = game_objs[f'{kind}s'][obj_id]
            text = f"{text}\n\t{entity.name}"
    return text

from app.container import Container

def process_event(event, game_objs):
    for trigger_data in event.triggers:
        trigger_object_kind, trigger_object_id = trigger_data.object
        trigger_obj = game_objs[f'{trigger_object_kind}s'][trigger_object_id]
        
        # Check if the trigger change condition for state is met
        if trigger_data.conditions.get('state', False):
            state_conditions = trigger_data.conditions['state']
            if 'is' in state_conditions and trigger_obj.state != state_conditions['is']:
                return f'{event.name} failed state is'
            if 'is_not' in state_conditions and trigger_obj.state == state_conditions['is_not']:
                return f'{event.name} failed state is not'  # Return empty string if state condition is not met

        # Check if the trigger change condition for inventory is met
        if trigger_data.conditions.get('inventory', False) and isinstance(trigger_obj, Container):
            inventory_conditions = trigger_data.conditions['inventory']
            if 'item' in inventory_conditions:
                items = inventory_conditions['item']
                if not all(item in trigger_obj.inventory for item in items):
                    return f'{event.name} failed has {items}'  # Return empty string if not all items are in inventory
            if 'no_item' in inventory_conditions:
                no_items = inventory_conditions['no_item']
                if any(item in trigger_obj.inventory for item in no_items):
                    return f'{event.name} failed does not have {items}'  # Return empty string if some items are in inventory

    trigger_event(event, game_objs)
    return event.description  # Return event description after triggering the event

def trigger_event(event, game_objs):
    # Check if there are affected objects and apply changes to them
    if event.affected_objects:
        for affected_kind, affected_id in event.affected_objects:
            affected = game_objs[f'{affected_kind}s'][affected_id]

            # Apply state change logic to affected objects
            if event.change.state:
                affected.state = event.change.state

            # Apply inventory change logic to affected objects if it's a Container
            if event.change.inventory and isinstance(affected, Container):
                inventory_change = event.change.inventory
                for add_item in inventory_change.add:
                    affected.inventory.append(add_item)
                for remove_item in inventory_change.remove:
                    if remove_item in affected.inventory:
                        affected.inventory.remove(remove_item)



def playing(stdscr, game_state: dict[str, any], game_objs: dict[str, dict[str, GameObject]]) -> dict[str, any]:
    obj_id = game_state["current_location"]
    location = game_objs["locations"][obj_id]
    text = generate_location_text(location, game_objs)
    command = game_state.get('user_command', '')
    processor = ActionProcessor()

    if 'events' in game_objs:
        events = game_objs['events']
        for obj_id in events.keys():
            if events[obj_id].state == 'active':
                #text = f'{text}\n{events[key].description}'
                text = f'{text}\n{process_event(events[obj_id], game_objs)}'

    if command and command != '':
        result = processor.process(command[0],location, game_objs, game_state, *command[1:])
        if isinstance(result, str):
            text = generate_location_text(location, game_objs)
            text = f'{text}\n\n {result}'
        elif isinstance(result, tuple):
            kind, target_obj_id = result
            if kind == 'location':
                game_state['current_location'] = target_obj_id
                location = game_objs["locations"][target_obj_id]
                text = generate_location_text(location, game_objs)
        game_state['previous_text'] = text
    if not command:
        text = game_state.get('previous_text', text)


    stdscr.addstr(1,0, f'{text}')
    game_state["location_name"] = location.name
    return game_state

def main(stdscr):
    # Set up the screen
    curses.curs_set(1)
    desired_height = 80
    desired_width = 200

    resize_terminal(desired_height, desired_width)

    stdscr.clear()
    stdscr.refresh()

    # Initalize the parser
    parser = Parser()

    data = load_data()
    game_objects = load_game_objects(data)
    input_text = ""
    height, width = stdscr.getmaxyx()
    input_window_row = height - 1
    input_window = curses.newwin(1, width, input_window_row, 0)

    scenes = {
        'title': title,
        'opening': opening,
        'help': help_func,
        "map" : map_func,
        "playing": playing
            }

    game_state = {}

    game_state["current_scene"] = "title"
    game_state["current_location"] = 1
    game_state["location_name"] = ''
    
    pygame.mixer.init()
    game_state["music_mixer"] = pygame.mixer
    game_state['songs'] = f"{'/'.join(os.path.abspath(__file__).split('/')[:-1])}/data/echoes-of-time-v2-by-kevin-macleod-from-filmmusic-io.mp3"
    game_state['music_mixer'].music.load(game_state['songs'])
    game_state['music_volume'] = 0.5
    game_state['music_mixer'].music.set_volume(0.5)
    game_state['music_playing'] = False
    # Inside the main function, before entering the game loop
    if not game_state['music_playing']:
        game_state['music_mixer'].music.play(-1)  # Play the music indefinitely (-1)
        game_state['music_playing'] = True

    while True:
        if game_state["current_scene"] == "playing":
            game_state = scenes[game_state["current_scene"]](stdscr, game_state, game_objects)

        else:
            scenes[game_state["current_scene"]](stdscr, data[game_state["current_scene"]])
        if not input_text:
            input_text = ''
        input_window.addstr(0, 0, f"{game_objects['players'][0].state}@{game_state.get('location_name', '')}>{input_text}")
        if game_state.get('user_command', ''):
            stdscr.addstr(height - 2 , 0, ' '.join(game_state['user_command']))
        stdscr.refresh()

        # Get the key pressed by the user
        key = input_window.getch()
        if key:
            game_state['user_command'] = None
            # Check for Enter key (key code 10) to clear the input text
            if key == 10:
                if game_state["current_scene"] == 'help':
                    game_state["current_scene"] = game_state["previous_scene"]
                    game_state["previous_scene"] = 'help'
                if game_state["current_scene"] == 'map':
                    game_state["current_scene"] = game_state["previous_scene"]
                    game_state["previous_scene"] = 'map'
                if game_state["current_scene"] == "opening":
                    game_state["current_scene"] = "playing"
                if input_text:
                    parsed_text = parser.parse(input_text)
                    if parsed_text:
                        if "start" == parsed_text[0]:
                            if game_state["current_scene"] == 'title':
                                game_state["current_scene"] = 'opening'
                        elif 'quit' == parsed_text[0]:
                            break
                        elif "help" == parsed_text[0]:
                            game_state["previous_scene"] = game_state["current_scene"]
                            game_state["current_scene"] = 'help'
                        elif 'goto' == parsed_text[0] and game_state["current_scene"] == "playing" and game_state.get('god_mode', False):
                            if len(parsed_text) > 1 and parsed_text[1].isdigit():
                                target_location = int(parsed_text[1])
                                if target_location in game_objects['locations'].keys():
                                    game_state["current_location"] = target_location
                        elif "map" == parsed_text[0]:
                            game_state["previous_scene"] = game_state["current_scene"]
                            game_state["current_scene"] = 'map'
                        elif 'poweroverwhelming' == parsed_text[0] and game_state["current_scene"] == "playing":
                            if not game_state.get('god_mode', False):
                                game_state['god_mode'] = True
                            else:
                                game_state['god_mode'] = False
                        elif "music" == parsed_text[0] and game_state["current_scene"] != "playing":
                            processor = ActionProcessor()
                            result = processor.process(parsed_text[0],None, None, game_state, *parsed_text[1:])
                            stdscr.addstr(height - 4,0, f'{result}')
                        else:
                            game_state['user_command'] = parsed_text
                input_text = ''


            # Check for Backspace key (key code 127) and non-empty input_text to delete characters
            elif key == 127 and input_text:
                input_text = input_text[:-1]

            # Accept printable ASCII characters (from space to tilde) and append to input_text
            elif 32 <= key <= 126:
                input_text += chr(key)


        stdscr.refresh()
        stdscr.clear()


if __name__ == '__main__':
    curses.wrapper(main)

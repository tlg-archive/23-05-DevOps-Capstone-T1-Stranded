#! /usr/bin/env python3
# James L. Rogers | github.com/DarkWinged


#imports
import curses
import os
import platform
import json
from app.npc import npc as Npc
from app.parser import Parser
from app.location import location as Location
from app.item import item as Item
from app.game_object import game_object
from app.action_processor import Action_Processor
from app.transition import Transition
from app.player import player as Player
from app.container import container as Container


def load_data() -> dict[str, any]:
    data = {}
    with open(f"{'/'.join(os.path.abspath(__file__).split('/')[:-1])}/data/title.txt", 'r') as title_file:
        data['title'] = title_file.readlines()
    
    with open(f"{'/'.join(os.path.abspath(__file__).split('/')[:-1])}/data/description.txt", "r") as plot:
        plot = plot.read().splitlines()
    plot_splice = []
    splice_len = 50
    for i in range(0, len(plot), splice_len):
        plot_splice.append(plot[i:i+splice_len])    
    data['opening'] = plot_splice

    with open(f"{'/'.join(os.path.abspath(__file__).split('/')[:-1])}/data/help.txt", "r") as help:
        data['help'] = help.read()

    object_types = ['locations', 'items', 'transitions', 'players', 'containers', 'npcs']

    for object_type in object_types:
        with open(f"{'/'.join(os.path.abspath(__file__).split('/')[:-1])}/data/{object_type}.json", "r") as loading:
            data[object_type] = json.load(loading)
    
    return data

def load_game_objects(data: dict[str, any]):
    objects = {}

    
    objects['npcs'] = {}
    for npc in data['npcs']:
        items = []
        if "inventory" in npc.keys():
            for item in npc['inventory']: 
                items.append((item['kind'], item['id']))
        npc_obj = Npc(npc['id'], npc['name'], npc['description'], npc['state'], npc['dialogue'], items )
        objects['npcs'][npc_obj.id] = npc_obj

    objects['locations'] = {}
    for location in data['locations']:
        entities = []
        if 'entities' in location.keys():
            for entity in location['entities']:
                entities.append((entity['kind'], entity['id']))
        location_obj = Location(location['id'], location['name'], location['description'], entities)
        objects['locations'][location_obj.id] = location_obj
        
    objects['items'] = {}
    for item in data['items']:
        item_obj = Item(item['id'], item['name'], item['description'], None)
        objects['items'][item_obj.id] = item_obj

    objects['transitions'] = {}
    for transition in data['transitions']:
        target = (transition['target']['kind'], transition['target']['id'])
        transition_obj = Transition(transition['id'], transition['name'], transition['description'], None, target)
        objects['transitions'][transition_obj.id] = transition_obj

    objects['players'] = {}
    for player in data['players']:
        inventory = []
        if player.get('inventory', []):
            for item in player['inventory']:
                inventory.append((item['kind'], item['id']))
        player_obj = Player(player['id'], player['name'], player['description'], player['state'], inventory)
        objects['players'][player_obj.id] = player_obj

    objects['containers'] = {}
    for container in data['containers']:
        inventory = []
        if container.get('inventory', []):
            for item in container['inventory']:
                inventory.append((item['kind'], item['id']))
        container_obj = Container(container['id'], container['name'], container['description'], container['state'], inventory)
        objects['containers'][container_obj.id] = container_obj

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

    message = "Enter start to play"
    stdscr.addstr(10, (width - len(message)) // 2, message)     

def opening(stdscr, data: list[list[str]]): 
    height, width = stdscr.getmaxyx()

    for index, string_list in enumerate(data):
        for string_index, string in enumerate(string_list):
            stdscr.addstr(5 + index + string_index, (width - len(string)) // 2, string)

def help(stdscr, data: str):
    stdscr.addstr(1,0, f'{data}')

def generate_location_text(location: Location, game_objs: dict[str, game_object]) -> str:
    text = f"{location.description}\n"
    if location.entities:
        text = f'{text}\nAround you you can see:'
        for kind, id in location.entities:
           entity = game_objs[f'{kind}s'][id]
           text = f"{text}\n\t{entity.name}" 
    return text

def playing(stdscr, game_state: dict[str, any], game_objs: dict[str, game_object]) -> dict[str, any]:
    id = game_state["current_location"]
    location = game_objs["locations"][id]
    text = generate_location_text(location, game_objs)
    command = game_state.get('user_command', '')
    processor = Action_Processor()    
    
    if command:
        action = processor.process(command[0])
        if action:
            result = action(location, game_objs, *command[1:])
            if isinstance(result, str):
                text = f'{text}\n\n {result}'
            elif isinstance(result, tuple):
                kind, target_id = result
                if kind == 'location':
                    game_state['current_location'] = target_id
                    location = game_objs["locations"][target_id] 
                    text = generate_location_text(location, game_objs)

                    

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
        'help': help,
        "playing": playing
            }

    game_state = {}

    game_state["current_scene"] = "title" 
    game_state["current_location"] = 1
    game_state["location_name"] = ''

    while True:
        if game_state["current_scene"] == "playing":
            game_state = scenes[game_state["current_scene"]](stdscr, game_state, game_objects)

        else:
            scenes[game_state["current_scene"]](stdscr, data[game_state["current_scene"]])
        if not input_text:
            input_text = '' 
        input_window.addstr(0, 0, f"{game_state.get('location_name', '')}>{input_text}")
        if game_state.get('user_command', ''):
            stdscr.addstr(height - 2 , 0, ' '.join(game_state['user_command']))
        stdscr.refresh()

        # Get the key pressed by the user
        key = input_window.getch()
    
        if key:
            # Check for Enter key (key code 10) to clear the input text
            if key == 10:
                if game_state["current_scene"] == 'help':
                    game_state["current_scene"] = game_state["previous_scene"]
                    game_state["previous_scene"] = 'help'
                if game_state["current_scene"] == "opening":
                    game_state["current_scene"] = "playing" 
                if input_text:
                    if "start" == parser.parse(input_text)[0]:
                        if game_state["current_scene"] == 'title':
                            game_state["current_scene"] = 'opening'
                    elif 'quit' == parser.parse(input_text)[0]:
                        break
                    elif "help" == parser.parse(input_text)[0]:
                        game_state["previous_scene"] = game_state["current_scene"]
                        game_state["current_scene"] = 'help'                  
                    else:
                       game_state['user_command'] = parser.parse(input_text) 
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

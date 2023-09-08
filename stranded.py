#! /usr/bin/env python3
# James L. Rogers | github.com/DarkWinged


#imports
import curses
import os
import platform
from app.parser import Parser

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

    return data

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
    input_text = ""    
    height, width = stdscr.getmaxyx()
    input_window_row = height - 1
    input_window = curses.newwin(1, width, input_window_row, 0)

    scenes = {
        'title':title,
        'opening':opening,
        'help':help
            }

    current_scene = 'title'

    while True:
        scenes[current_scene](stdscr, data[current_scene])
        stdscr.refresh()

        # Get the key pressed by the user
        key = input_window.getch()
    
        if key:
            # Check for Enter key (key code 10) to clear the input text
            if key == 10:
                if current_scene == 'help':
                    current_scene = previus_scene
                    previus_scene = 'help'
                if input_text:
                    stdscr.addstr(height - 2 , 0, ' '.join(parser.parse(input_text)))
                    if "start" == parser.parse(input_text)[0]:
                        if current_scene == 'title':
                            current_scene = 'opening'
                    elif 'quit' == parser.parse(input_text)[0]:
                        break
                    elif "help" == parser.parse(input_text)[0]:
                        previus_scene = current_scene
                        current_scene = 'help'                  
                input_text = ''

        
            # Check for Backspace key (key code 127) and non-empty input_text to delete characters
            elif key == 127 and input_text:
                input_text = input_text[:-1]
        
            # Accept printable ASCII characters (from space to tilde) and append to input_text
            elif 32 <= key <= 126:
                input_text += chr(key)

        input_window.addstr(0, 0, f">{input_text}")

        stdscr.refresh()
        stdscr.clear()


if __name__ == '__main__':
    curses.wrapper(main)

#! /usr/bin/env python3
# James L. Rogers | github.com/DarkWinged


#imports
import curses
import os
from app import parser as Parser

def main(stdscr):
    # Set up the screen
    curses.curs_set(1)
    desired_height = 30
    desired_width = 175

    # Resize the terminal window
    curses.resizeterm(desired_height, desired_width)
    stdscr.clear()
    stdscr.refresh()

    parser = Parser.Parser()

    # Get the screen dimensions
    height, width = stdscr.getmaxyx()
    with open(os.path.abspath('./data/title.txt'), 'r', encoding='utf-8') as title_file:
        title_lines = title_file.readlines()
    with open("./data/description.txt", "r") as plot:
        plot = plot.read().splitlines()
        plot_splice = []
        splice_len = 50
        for i in range(0, len(plot), splice_len):
            plot_splice.append(plot[i:i+splice_len])

    input_text = ""    
    height, width = stdscr.getmaxyx()
    input_window_row = height - 1
    input_window = curses.newwin(1, width, input_window_row, 0)

    game_state_started = False

    while True:
        # Clear the windows
        stdscr.clear()
        
        input_window.addstr(0, 0, f">{input_text}")

        if not game_state_started:        
            for index, line in enumerate(title_lines):
                stdscr.addstr(index, (width - len(line)) // 2, f'{line}')

            for i, string_list in enumerate(plot_splice):
                for j, string in enumerate(string_list):
                    stdscr.addstr(i + len(title_lines) + j, (width - len(string)) // 2, string)
            stdscr.addstr(10,0, "Enter start to play")     
        else:
            pass
        # Get the key pressed by the user
        key = input_window.getch()
    

        # Check for Enter key (key code 10) to clear the input text
        if key == 10:
            stdscr.addstr(height - 2 , 0, ' '.join(parser.parse(input_text)))
            if "start" == parser.parse(input_text)[0]:
                game_state_started = True
                stdscr.clear()
            elif 'quit' == parser.parse(input_text)[0]:
                break
            input_text = ''
        
        # Check for Backspace key (key code 127) and non-empty input_text to delete characters
        elif key == 127 and input_text:
            input_text = input_text[:-1]
        
        # Accept printable ASCII characters (from space to tilde) and append to input_text
        elif 32 <= key <= 126:
            input_text += chr(key)
        stdscr.refresh()


if __name__ == '__main__':
    curses.wrapper(main)

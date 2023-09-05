#! /usr/bin/env python3
# James L. Rogers | github.com/DarkWinged


#imports
import curses
import os

def main(stdscr):
    # Set up the screen
    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()
  
    # Get the screen dimensions
    height, width = stdscr.getmaxyx()
    with open(os.path.abspath('./data/title.txt'), 'r', encoding='utf-8') as title_file:
        title_lines = title_file.readlines()
    
    while True:
        # Clear the windows
        stdscr.clear()

        stdscr.refresh()

        for index, line in enumerate(title_lines):
            stdscr.addstr(index, (width - len(line)) // 2, f'{line}')
        stdscr.refresh()



def display_strings(stdscr, plot):
    # Initialize curses
    curses.curs_set(0)  # Hide the cursor
    stdscr.clear()
    stdscr.refresh()
    with open("./data/description", "r") as plot:
        plot = plot.read().splitlines()
    for i, string in enumerate(plot):
        stdscr.addstr(i, 0, string.strip())
        stdscr.refresh()
        stdscr.getch()
def main(stdscr):
    curses.wrapper(display_strings, "strings.txt")
if __name__ == '__main__':
    curses.wrapper(main)

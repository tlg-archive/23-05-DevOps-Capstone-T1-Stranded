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
    with open("./data/description", "r") as plot:
        plot = plot.read().splitlines()
        plot_splice = []
        splice_len = 50
        for i in range(0, len(plot), splice_len):
            plot_splice.append(plot[i:i+splice_len])
        
    while True:
        # Clear the windows
        stdscr.clear()

        stdscr.refresh()

        for index, line in enumerate(title_lines):
            stdscr.addstr(index, (width - len(line)) // 2, f'{line}')
        stdscr.refresh()
        for i, string_list in enumerate(plot_splice):
            for j, string in enumerate(string_list):
                stdscr.addstr(i + len(title_lines) + j, (width - len(string)) // 2, string)

            #stdscr.addstr(i + len(title_lines), (width - len(line)) // 2 , string.strip())
        stdscr.refresh()
        stdscr.getch()

if __name__ == '__main__':
    curses.wrapper(main)
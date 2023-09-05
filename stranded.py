#! /usr/bin/env python3
# James L. Rogers | github.com/DarkWinged


#imports
import curses

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

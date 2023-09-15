import sys
import stranded
import curses

if __name__ == "__main__":
    try:
        # Use curses.wrapper to run stranded.main
        curses.wrapper(stranded.main)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

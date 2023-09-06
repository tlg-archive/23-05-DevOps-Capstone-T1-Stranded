import curses
import os

def main(stdscr):
    # Set up the screen
    curses.curs_set(1)  # Enable cursor for input
    stdscr.clear()
    stdscr.refresh()

    # Get the screen dimensions
    height, width = stdscr.getmaxyx()

    # Read title text
    with open(os.path.abspath('./data/title.txt'), 'r', encoding='utf-8') as title_file:
        title_lines = title_file.readlines()

    # Calculate the vertical position for title text
    title_start_y = (height - len(title_lines)) // 2

    # Read description text
    with open("./data/description.txt", "r") as plot_file:
        description_lines = plot_file.read().splitlines()

    # Define the bottom text for the title screen
    bottom_text = "Press 's' to start or 'q' to quit."

    # Display initial title screen
    for index, line in enumerate(title_lines):
        stdscr.addstr(title_start_y + index, (width - len(line)) // 2, f'{line}')

    # Display the alternate text under the title
    alternate_text = "Press 's' again to explore space or 'q' to quit."
    stdscr.addstr(title_start_y + len(title_lines) + 2, (width - len(alternate_text)) // 2, alternate_text)

    stdscr.refresh()

    while True:
        user_input = stdscr.getch()  # Get user input without blocking

        if user_input == ord("q"):  # Check for 'q' key to quit
            break

        if user_input == ord("s"):  # Check for 's' key to start
            # Clear the previous text
            stdscr.clear()

            # Calculate the horizontal position to center each line of description text
            description_y = (height - len(description_lines)) // 2

            # Display description text in a square block
            for line in description_lines:
                x_description = (width - len(line)) // 2
                stdscr.addstr(description_y, x_description, line)
                description_y += 1

            # Display the instruction to type 'gone' to quit
            quit_instruction = "To exit, type 'gone' and press Enter."
            stdscr.addstr(1, 1, quit_instruction)
            
            stdscr.refresh()

            # Wait for user input on the description screen
            while True:
                user_input = stdscr.getch()
                if user_input == ord("q"):  # Check for 'q' to quit
                    break
                elif user_input == ord("s"):  # Check for 's' to transition to the new screen
                    stdscr.clear()

                    # Description of space
                    space_description = """
                    A blur of alarms, the whine of the siren, the ship rocking to its side, the terminal had sounded an alarm briefly before an 
		    energy salvo hit the aft side of the ship. Running, the hatch to the escape pod closing….  

		     My thoughts were of fear before settling into a growing sense of elation. The pods' alarms were blaring and the interface before me 
	             both told me the same thing: I had crashed. I had lived, I was alive. The escape pod had made it through the atmosphere past the asteroids 
	             that had ripped through my cargo ship and judging by the readout of the sensors, the air was breathable and I had hit land. It was good to 
                     see the autonomous survival system in the pod had done its job, I disconnected my seat restraints.
                    """
                    stdscr.addstr((height - len(space_description.splitlines())) // 2, 0, space_description)

                    # Display a command line for user input
                    command_line = "> "
                    stdscr.addstr(height - 1, 0, command_line)
                    stdscr.move(height - 1, len(command_line))
                    stdscr.refresh()

                    # Wait for user input on the space description screen
                    while True:
                        user_input = stdscr.getch()
                        if user_input == ord("q"):  # Check for 'q' to quit
                            break
                        elif user_input == ord("s"):  # Check for 's' to start again
                            break
                        elif user_input == ord("g"):  # Check for 'g' to initiate quitting
                            # Check if the user types 'gone' to quit
                            user_input = stdscr.getch()
                            if user_input == ord("o"):
                                user_input = stdscr.getch()
                                if user_input == ord("n"):
                                    user_input = stdscr.getch()
                                    if user_input == ord("e"):
                                        return  # Quit the application

                    stdscr.clear()
                    # Redisplay the description screen if 's' was pressed
                    if user_input == ord("s"):
                        description_y = (height - len(description_lines)) // 2
                        for line in description_lines:
                            x_description = (width - len(line)) // 2
                            stdscr.addstr(description_y, x_description, line)
                            description_y += 1
                        stdscr.addstr(1, 1, quit_instruction)
                        stdscr.addstr(height - 1, 0, command_line)
                        stdscr.move(height - 1, len(command_line))
                        stdscr.refresh()

# Run the curses application
if __name__ == "__main__":
    curses.wrapper(main)


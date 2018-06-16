import curses
import os

from .UiConsts import color_pairs
from .Widgets.ServerList import *

class UiManager:
    # Initializes colors for console
    def init_colors():
        curses.init_pair(color_pairs["window_selected"], curses.COLOR_YELLOW, 0)
        curses.init_pair(color_pairs["item_selected"], 0, curses.COLOR_YELLOW)

    def __init__(self):
        self.widgets = []
        self.focused_index = -1 # -1 equals none widgets are focused

        os.environ.setdefault('ESCDELAY', '25') # Disables escape sequences for Linux and Mac

        curses.wrapper(self.main)

    # Moves focus to the next widget
    def move_focus(self):
        self.focused_index += 1

        # Wrap index around widget list
        self.focused_index %= len(self.widgets)

        self.focus_single_widget(self.focused_index)

    # Focus widget while defocusing others
    # Use -1 to defocus all widgets
    def focus_single_widget(self, focus_ind):
        for ind, widget in enumerate(self.widgets):
            widget.focus(ind == focus_ind)
            widget.refresh()

        self.focused_index = focus_ind

    def log(self, a):
        self.focus_single_widget(-1)

    def main(self, stdscr):
        curses.curs_set(False)

        UiManager.init_colors()

        stdscr.clear()

        # Create server list
        server_list = ServerList(0, 0, curses.LINES, 20)
        self.widgets.append(server_list)

        # Debug event
        listener = EventListener(self, self.log)
        server_list.server_chosen_event.add(listener)

        # Debug input for list
        server_names = [
            'Server',
            'Server Too',
            'Best Server',
            'Worst Server',
            'Just Server',
            'Super Long Server Name For NO Reason At All',
        ]

        for server_name in server_names:
            s_data = ServerData()
            s_data.display_name = server_name
            server_list.add_item(s_data)

        # Create debug char window
        chat_window = Widget(0, 20, curses.LINES, curses.COLS - 21)
        self.widgets.append(chat_window)

        stdscr.refresh()

        for widget in self.widgets:
            widget.refresh()

        # Main loop? Should be redesigned
        while (True):
            c = stdscr.getch()
            if c == ord('\t'): # Tab to move focus between widgets
                self.move_focus()
            elif c == 27: # ESC to defocus all widgets
                self.focus_single_widget(-1)
            elif c == ord('q'):
                break  # Q to exit UI
            else:
                # Send input to focused widget
                if self.focused_index >= 0:
                    self.widgets[self.focused_index].on_char_pressed(c)

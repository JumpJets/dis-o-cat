from ..UiConsts import color_pairs, trunc_string

from .Widget import *

# Class for storing and displaying list
# Supports user input
class ItemList(Widget):
    def __init__(self, y, x, height, width):
        # Initialize widget
        super().__init__(y, x, height, width)

        # Initialize item list variables
        self.item_list = []
        self.selected_index = -1 # -1 means selected none

    # On char pressed
    def on_char_pressed(self, ch):
        if ch == curses.KEY_UP:
            self.select_next_item(-1)
        elif ch == curses.KEY_DOWN:
            self.select_next_item()
        else:
            super().on_char_pressed(ch)

        self.refresh()

    # Adds item to item list
    def add_item(self, item):
        self.item_list.append(item)

    # Select item at index
    # Use -1 index to deselect all items
    def select_item(self, ind):
        # Clamp index at allowed index range
        ind = max(min(ind, len(self.item_list)), -1)

        self.selected_index = ind

    # Returns selected
    def get_selected_index(self):
        return self.selected_index

    # Select next item in list, wrapping around
    # Supports negative step
    def select_next_item(self, step=1):
        self.selected_index += step
        self.selected_index %= len(self.item_list)

        self.select_item(self.selected_index)

    # Draws item at provided index
    def __draw_item(self, idx, attr=0):
        # Truncate item if too large
        max_item_size = self.window.getmaxyx()[1] - self.padding[1] - self.padding[3]
        trunc_item = self.item_list[idx]
        if len(trunc_item) > max_item_size:
            trunc_item = trunc_item[:(max_item_size - len(trunc_string))] + trunc_string

        # Add spaces if item is too short (for colorful background)
        trunc_item = format(trunc_item, '<' + str(max_item_size))

        self.window.addstr(self.padding[0] + idx, self.padding[3], trunc_item, attr)

    # Refreshes item list area
    def refresh(self):
        # Update widget
        super().refresh()

        # Display items
        for idx, item in enumerate(self.item_list):
            # Stop if there is no space left in widget
            line = self.padding[0] + idx
            if line >= self.window.getmaxyx()[0] - self.padding[2]:
                break

            self.__draw_item(idx)

        # Redraw selected item if widget is focused
        if self.selected_index >= 0:
            if self.focused:
                self.__draw_item(self.selected_index, curses.color_pair(color_pairs['item_selected']))
            else:
                self.__draw_item(self.selected_index, curses.A_REVERSE)

        # Display changes on screen
        self.window.refresh()

import curses

from ..UiConsts import color_pairs

# Base class for any application widgets
class Widget:
    def __init__(self, y, x, height, width):
        self.focused = False
        self.padding = (1, 1, 1, 1) # Excludes borders

        self.window = curses.newwin(height, width, y, x)

    # Focus widget
    def focus(self, focused=True):
        self.focused = focused
        self.on_focus_changed(self.focused)

    # Blur widget
    def blur(self):
        self.focus(False)

    # Virtual function to be called when focus changed
    def on_focus_changed(self, focus):
        pass

    # Virtual function to be called when char was pressed and input was directed to this widget
    def on_char_pressed(self, ch):
        pass

    # Refreshes widget area
    def refresh(self):
        # Draw border
        if self.focused:
            self.window.attron(curses.color_pair(color_pairs["window_selected"]))
        self.window.border()
        if self.focused:
            self.window.attroff(curses.color_pair(color_pairs["window_selected"]))

        self.window.refresh()

    # Returns pressed char
    def getch(self):
        return self.window.getch()

from .ItemList import *

from ..UiEvent import *

class ServerData:
    def __init__(self):
        self.name = 'ERROR_NAME'
        self.display_name = 'ERROR_DISPLAY_NAME'
        self.server_id = -1

class ServerList(ItemList):
    def __init__(self, y, x, height, width):
        super().__init__(y, x, height, width)

        self.server_list = []
        self.server_chosen_event = Event()
        self.selected_server_ind = -1

    # Adds server to server list
    def add_item(self, item):
        if isinstance(item, ServerData):
            super().add_item(item.display_name)
            self.server_list.append(item)
        else:
            super().add_item('NOT SERVER DATA TYPE')
            self.server_list.append(ServerData())

    # Selects server?
    def select_server(self, ind):
        if ind < 0 or ind > len(self.server_list):
            pass

        self.selected_server_ind = ind
        self.server_chosen_event.emit(self.server_list[ind])
        self.blur()

    def on_char_pressed(self, ch):
        if ch == curses.KEY_ENTER or ch == ord('\n') or ch == ord('\r'):
            self.select_server(self.get_selected_index())
        else:
            super().on_char_pressed(ch)

    def on_focus_changed(self, focus):
        self.select_item(self.selected_server_ind)

class Event(set):
    def __init__(self, *args):
        super(Event, self).__init__(*args)

    def emit(self, *args):
        for listener in self:
            listener.call(*args)

class EventListener:
    def __init__(self, owner, callback):
        self.owner = owner
        self.callback = callback

    def call(self, *args):
        self.callback(self.owner, *args[1:])

class Event(set):
    def __init__(self, *args, **kwargs):
        super(Event, self).__init__(*args, **kwargs)

    def emit(self, *args, **kwargs):
        for listener in self:
            listener.call(*args, **kwargs)

class EventListener:
    def __init__(self, owner, callback):
        self.owner = owner
        self.callback = callback

    def call(self, *args, **kwargs):
        self.callback(self.owner, *args[1:], **kwargs)

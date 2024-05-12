class Event(object):
    def __init__(self):
        self.name = "Generic event"

    def __str__(self):
        return self.name


class QuitEvent(Event):
    def __init__(self):
        self.name = "Quit event"


class TickEvent(Event):
    def __init__(self):
        self.name = "Tick event"


class MenuItemSelectionChangedEvent(Event):
    def __init__(self, increase=True):
        self.name = "Item selection changed event"
        self.increase = increase


class MenuItemSelectedEvent(Event):
    def __init__(self):
        self.name = "Menu item selected event"


class InputEvent(Event):
    def __init__(self, key):
        self.name = "Input event"
        self.char = key

    # def __str__(self):
        # return '%s, char=%s' % (self.name, self.char)


class ModifierAppliedEvent(Event):
    def __init__(self, modifier):
        self.name = "Modifier applied event"
        self.modifier = modifier


class InitializeEvent(Event):
    def __init__(self):
        self.name = "Initialize event"


class StateChangeEvent(Event):
    def __init__(self, state):
        self.name = "Game state change event"
        self.state = state

    def __str__(self):
        if self.state:
            return '%s pushed %s' % (self.name, self.state)
        else:
            return '%s popped' % (self.name,)


# Coordinator between MVC layers
class EventBus(object):
    def __init__(self):
        from weakref import WeakKeyDictionary
        self.listeners = WeakKeyDictionary()

    def register_listener(self, listener):
        self.listeners[listener] = 1

    def unregister_listener(self, listener):
        if listener in self.listeners.keys():
            del self.listeners[listener]

    def post(self, event):
        # if not isinstance(event, TickEvent):
            # debug print the event if it is not TickEvent
            # print(str(event))
        for listener in self.listeners.keys():
            listener.notify(event)

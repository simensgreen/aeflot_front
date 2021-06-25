import enum


class AppEvent(enum.Enum):
    ConfigChanged = enum.auto()
    PlanesChanged = enum.auto()
    ModelChanged = enum.auto()
    HistoryChanged = enum.auto()
    ExitApp = enum.auto()


class Handlers:
    def __init__(self):
        self.__handlers = {key: [] for key in AppEvent}
        self.__handlers_ids = {0: lambda: None}

    def add(self, handler: callable, event: AppEvent, priority=0):
        tmp = self.next_id
        self.__handlers[event].append((tmp, priority))
        self.__handlers_ids[tmp] = handler
        return tmp

    def remove(self, handler_id, event: AppEvent = None):
        if event is None:
            for app_event in AppEvent:
                self.remove(handler_id, app_event)
        else:
            self.__handlers[event] = [value for value in self.__handlers[event] if value[0] != handler_id]
            self.__handlers_ids.pop(handler_id, None)

    def call(self, event: AppEvent):
        for handler in sorted(self.__handlers[event], key=lambda val: -val[1]):
            self.__handlers_ids[handler[0]]()

    @property
    def next_id(self):
        return max(self.__handlers_ids.keys()) + 1

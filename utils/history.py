import datetime
import enum
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

from utils import Logger
from utils.command import Command
from utils.handlers import AppEvent, Handlers


@dataclass
class Task:
    event: "Event"
    target: "EventStatus"
    log: Logger

    def __call__(self, *args, **kwargs):
        if self.target == EventStatus.DONE:
            self.log.dbg(f'Выполнение команды {self.event.command}')
            self.event.command.do()
            self.event.status = self.target
            self.log.info(f'Команда выполенена {self.event.command}')
        elif self.target == EventStatus.CANCELLED:
            self.log.dbg(f'Отмена команды {self.event.command}')
            self.event.command.undo()
            self.event.status = self.target
            self.log.info(f'Команда отменена {self.event.command}')


class EventStatus(enum.Enum):
    DONE = enum.auto()
    CANCELLED = enum.auto()
    PROCESSING = enum.auto()


@dataclass
class Event:
    command: Command
    date: datetime.datetime = field(default_factory=datetime.datetime.today)
    status: EventStatus = field(default=EventStatus.PROCESSING)


class History:
    def __init__(self, log: Logger, handlers: Handlers):
        self.__commands = []
        self.log = log
        self.executor = ThreadPoolExecutor()
        self.handlers = handlers

    def __iter__(self):
        return iter(self.commands)

    def find(self, command: Command) -> Optional[int]:
        try:
            return self.__commands.index(command)
        except ValueError:
            return None

    def get(self, index) -> Optional[Command]:
        try:
            return self.__commands[index]
        except IndexError:
            return None

    def add(self, command: Command) -> int:
        tmp = len(self.__commands)
        event = Event(command)
        Task(event, EventStatus.DONE, self.log)()
        self.__commands.append(event)
        self.handlers.call(AppEvent.HistoryChanged)
        return tmp

    def cancel(self, index: int) -> Optional[Command]:
        try:
            command = self.__commands[index]
            Task(command, EventStatus.CANCELLED, self.log)()
            self.handlers.call(AppEvent.HistoryChanged)
            return command
        except IndexError:
            self.log.err(f"Команда {index = } не найдена.")
            return None

    def cancel_last(self) -> Optional[Command]:
        if self.__commands:
            for event in reversed(tuple(self)):
                if event.status == EventStatus.DONE:
                    self.cancel(self.find(event))
                    return None
        else:
            self.log.warn("Нечего отменять")
            return None

    def remove(self, index) -> Optional[Command]:
        try:
            command = self.__commands.pop(index)
            self.handlers.call(AppEvent.HistoryChanged)
            return command
        except IndexError:
            self.log.err(f"Команда {index = } не найдена.")
            return None

    @property
    def commands(self):
        return sorted(self.__commands, key=lambda val: val.date)

    # def save(self, filename: str):
    #     with open(filename, 'wb') as file:
    #         pickle.dump(self.commands, file)
    #     self.log.info(f'История операций сохранена в {filename}')
    #
    # def load(self, filename: str):
    #     with open(filename, 'rb') as file:
    #         commands = pickle.load(file)
    #     self.log.info(f'История операций загружена из {filename}')
    #     for command in commands:
    #         self.add(command)

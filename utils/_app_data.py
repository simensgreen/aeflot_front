from configparser import ConfigParser
from dataclasses import dataclass

from core import Model
from ._logger import Logger
from .handlers import Handlers
from .history import History


@dataclass(repr=False)
class AppData:
    model: Model
    config: ConfigParser
    history: History
    logger: Logger
    handlers: Handlers

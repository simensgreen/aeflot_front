import logging
from configparser import SectionProxy

from PyQt5.QtWidgets import QStatusBar


class Logger:
    def __init__(self, config: SectionProxy, status_bar: QStatusBar = None):
        self.config = config
        self.update_config()
        self.__logger = logging.getLogger("")
        self.status_bar = status_bar
        self.dbg(f'Инициализация системы логирования завершена успешно с уровнем {self.level}')

    def dbg(self, message: str, exc_info=False, msecs=2000):
        if self.status_bar and 0 <= self.level:
            self.status_bar.showMessage(f"DEBUG: {message}", msecs=msecs)
        self.__logger.debug(message, exc_info=exc_info)

    def info(self, message: str, exc_info=False, msecs=5000):
        if self.status_bar and 1 <= self.level:
            self.status_bar.showMessage(f"Информация: {message}", msecs=msecs)
        self.__logger.info(message, exc_info=exc_info)

    def warn(self, message: str, exc_info=False, msecs=0):
        if self.status_bar and 2 <= self.level:
            self.status_bar.showMessage(f"Предупреждение: {message}", msecs=msecs)
        self.__logger.warning(message, exc_info=exc_info)

    def err(self, message: str, exc_info=False, msecs=0):
        if self.status_bar and 3 <= self.level:
            self.status_bar.showMessage(f"Ошибка: {message}", msecs=msecs)
        self.__logger.error(message, exc_info=exc_info)

    @property
    def level(self):
        return int(self.config['level'])

    def update_config(self):
        if self.config['filename']:
            logging.basicConfig(filename=self.config['filename'], filemode=self.config['filemode'])
        logging.basicConfig(level=self.config.getint('level'), format=self.config['format'])

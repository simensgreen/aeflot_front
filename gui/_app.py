import copy
import os
import sys
from configparser import ConfigParser, ExtendedInterpolation

import OpenGL.GL as OGL
from PyQt5.QtWidgets import QApplication

from core import Model
from core.model_commands import NormalizeModelCommand, LoadModelCommand
from gui import AeflotFrontMainWindow
from utils import DEFAULT_CONFIG, AppData, History, Logger, Handlers, AppEvent


class AeflotFrontApp:
    @staticmethod
    def run():
        app = QApplication(sys.argv)
        config = copy.deepcopy(DEFAULT_CONFIG)
        user_config = False
        if os.path.exists('config.ini'):
            user_config = ConfigParser(interpolation=ExtendedInterpolation())
            user_config.read('config.ini')
            for section in config.sections():
                if section in user_config:
                    config[section].update(user_config[section])
            user_config = True
        logger = Logger(config['logging'])
        if user_config:
            logger.info("Настройки загружены из config.ini")
        handlers = Handlers()
        handlers.add(lambda: AeflotFrontApp.exit(logger), AppEvent.ExitApp, priority=-255)
        model = Model()
        app_data = AppData(model, config, History(logger, handlers), logger, handlers)
        if config['model']['startup model']:
            app_data.history.add(LoadModelCommand(config['model']['startup model'], app_data))
        if config['model'].getboolean("normalize on load"):
            app_data.history.add(NormalizeModelCommand(app_data))
        window = AeflotFrontMainWindow(app_data)
        window.show()
        app_data.logger.info('Приложение запущено')
        OGL.glEnable(OGL.GL_LINE_SMOOTH)
        sys.exit(app.exec_())

    @staticmethod
    def exit(logger=None):
        if logger:
            logger.info("Закрытие приложения")
        sys.exit(0)


if __name__ == '__main__':
    AeflotFrontApp.run()

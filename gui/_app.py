import sys
import os
import OpenGL.GL as OGL
from configparser import ConfigParser, ExtendedInterpolation

from PyQt5.QtWidgets import QApplication

from core import Model
from gui import AeflotFrontMainWindow
from utils import DEFAULT_CONFIG, AppData, History, Logger, Handlers, AppEvent


class AeflotFrontApp:
    @staticmethod
    def run():
        app = QApplication(sys.argv)
        if os.path.exists('config.ini'):
            config = ConfigParser(interpolation=ExtendedInterpolation())
            config.read('config.ini')
        else:
            config = DEFAULT_CONFIG
        logger = Logger(config['logging'])
        handlers = Handlers()
        handlers.add(lambda: AeflotFrontApp.exit(logger), AppEvent.ExitApp, priority=-255)
        app_data = AppData(Model(), config, History(logger, handlers), logger, handlers)
        window = AeflotFrontMainWindow(app_data)
        window.show()
        app_data.logger.info('Приложение запущено')
        sys.exit(app.exec_())

    @staticmethod
    def exit(logger=None):
        if logger:
            logger.info("Закрытие приложения")
            OGL.glEnable(OGL.GL_LINE_SMOOTH)
        sys.exit(0)


if __name__ == '__main__':
    AeflotFrontApp.run()

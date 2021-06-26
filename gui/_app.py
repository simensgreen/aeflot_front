import sys
import os
from configparser import ConfigParser, ExtendedInterpolation

from PyQt5.QtWidgets import QApplication

from core import Model
from core.model_commands import NormalizeModelCommand
from gui import AeflotFrontMainWindow
from utils import DEFAULT_CONFIG, AppData, History, Logger, Handlers, AppEvent
import OpenGL.GL as OGL


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
        model = Model()
        app_data = AppData(model, config, History(logger, handlers), logger, handlers)
        if config['model']['startup model']:
            model.load_model(config['model']['startup model'])
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

from PyQt5.QtWidgets import QMainWindow

from gui.docks import AeflotFrontDockArea
from gui.widgets import AeflotFrontMenuBar
from utils import AppData


class AeflotFrontMainWindow(QMainWindow):
    def __init__(self, app_data: AppData):
        super().__init__()
        self.app_data = app_data
        self.app_data.logger.status_bar = self.statusBar()

        config = self.app_data.config['window']
        self.setWindowTitle(config['title'])
        self.setGeometry(config.getint('x'), config.getint('y'), config.getint('width'), config.getint('height'))

        dock_area = AeflotFrontDockArea(self.app_data)
        self.setCentralWidget(dock_area)
        self.setMenuBar(AeflotFrontMenuBar(self.app_data, dock_area))

        self.app_data.logger.dbg("Инициализация интерфейса прошла успешно")

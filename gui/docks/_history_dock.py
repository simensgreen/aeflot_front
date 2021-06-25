from PyQt5.QtWidgets import QWidget
from pyqtgraph.dockarea import Dock

from utils import AppData, AppEvent


class HistoryDock(Dock):
    def __init__(self, app_data: AppData):
        super().__init__("История операций")
        self.widget = QWidget()
        self.addWidget(self.widget)
        self.app_data = app_data
        self.handler_id = app_data.handlers.add(self.update, AppEvent.HistoryChanged)

    def update(self):
        pass

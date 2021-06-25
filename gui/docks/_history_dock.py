from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from pyqtgraph.dockarea import Dock

from utils import AppData, AppEvent


class HistoryDock(Dock):
    def __init__(self, app_data: AppData):
        super().__init__("История операций")
        self.app_data = app_data
        self.widget = QTableWidget()
        self.widget.setColumnCount(3)
        self.widget.setRowCount(100)
        self.addWidget(self.widget)
        self.handler_id = app_data.handlers.add(self.update, AppEvent.HistoryChanged)

    def update(self):
        self.widget.clear()

        self.widget.setHorizontalHeaderLabels(("Время", "Команда", "Статус"))
        for no, event in enumerate(self.app_data.history):
            self.widget.setItem(no, 0, QTableWidgetItem(str(event.date)))
            self.widget.setItem(no, 1, QTableWidgetItem(str(event.command)))
            self.widget.setItem(no, 2, QTableWidgetItem(str(event.status)))

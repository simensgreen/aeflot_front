from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from pyqtgraph.dockarea import Dock

from utils import AppData, AppEvent


class PlanesListDock(Dock):
    def __init__(self, app_data: AppData):
        super().__init__("Плоскости")
        self.widget = QListWidget()
        self.addWidget(self.widget)
        self.app_data = app_data
        self.handler_id = app_data.handlers.add(self.update, AppEvent.PlanesChanged)
        self.items = []

    def add_plane(self, x):
        list_item = QListWidgetItem(f'{x = }')
        self.items.append(list_item)
        self.widget.addItem(list_item)

    def update(self):
        self.widget.clear()
        for plane in sorted(self.app_data.model.planes):
            self.add_plane(plane)

    def remove(self):
        self.app_data.handlers.remove(self.handler_id)
        self.deleteLater()

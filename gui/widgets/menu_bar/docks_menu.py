from PyQt5.QtWidgets import QMenu

from gui.docks import Docks, AddDockCommand
from gui.docks._dock_area import RemoveDockCommand
from utils import AppEvent


class DocksMenu(QMenu):
    def __init__(self, app_data, dock_area):
        super().__init__()
        self.dock_area = dock_area
        self.setTitle('Доки')
        self.app_data = app_data
        self.plane_settings = self.addAction("Настройки плоскости")
        self.plane_settings.setCheckable(True)
        self.plane_settings.triggered.connect(lambda val: self.manage_dock(val, Docks.PlaneSettings))
        self.axonometric = self.addAction('Аксонометрия')
        self.axonometric.setCheckable(True)
        self.axonometric.triggered.connect(lambda val: self.manage_dock(val, Docks.Axonometric))
        self.planes_list = self.addAction("Плоскости")
        self.planes_list.setCheckable(True)
        self.planes_list.triggered.connect(lambda val: self.manage_dock(val, Docks.PlanesListDock))
        self.history = self.addAction("История операций")
        self.history.setCheckable(True)
        self.history.triggered.connect(lambda val: self.manage_dock(val, Docks.HistoryDock))
        projections = self.addMenu("Проекции")
        self.projection_xz = projections.addAction("XZ")
        self.projection_xz.setCheckable(True)
        self.projection_xy = projections.addAction("XY")
        self.projection_xy.triggered.connect(lambda val: self.manage_dock(val, Docks.ProjectionXZ))
        self.projection_xy.setCheckable(True)
        self.projection_xy.setDisabled(True)
        self.projection_yz = projections.addAction("YZ")
        self.projection_yz.setCheckable(True)
        self.projection_yz.setDisabled(True)

        self.app_data.handlers.add(self.update, AppEvent.DocksChanged)
        self.update()

    def update(self):
        self.plane_settings.setChecked(Docks.PlaneSettings in self.app_data.docks)
        self.planes_list.setChecked(Docks.PlanesListDock in self.app_data.docks)
        self.history.setChecked(Docks.HistoryDock in self.app_data.docks)
        self.axonometric.setChecked(Docks.Axonometric in self.app_data.docks)
        self.projection_xz.setChecked(Docks.ProjectionXZ in self.app_data.docks)

    def manage_dock(self, add, dock):
        if add:
            self.add_dock(dock)
        else:
            self.remove_dock(dock)

    def add_dock(self, dock: Docks):
        self.app_data.history.add(AddDockCommand(self.dock_area, dock))

    def remove_dock(self, dock: Docks):
        self.app_data.history.add(RemoveDockCommand(self.dock_area, dock))

import enum

from pyqtgraph.dockarea import DockArea

from gui.docks._axonometric_dock import AxonometricDock
from gui.docks._history_dock import HistoryDock
from gui.docks._plane_settings_dock import PlaneSettingsDock
from gui.docks._planes_list_dock import PlanesListDock
from gui.docks._projection_dock import ProjectionDock
from utils import AppData, Command, AppEvent


class Docks(enum.Enum):
    Axonometric = enum.auto()
    PlaneSettings = enum.auto()
    ProjectionXZ = enum.auto()
    PlanesListDock = enum.auto()
    HistoryDock = enum.auto()


class AddDockCommand(Command):
    def __init__(self, area: "AeflotFrontDockArea", dock_type: Docks):
        self.dock_type = dock_type
        self.area = area

    def undo(self):
        if self.dock_type not in self.area.app_data.docks:
            return
        if self.dock_type == Docks.Axonometric:
            self.area.remove_axonometric()
        elif self.dock_type == Docks.PlaneSettings:
            self.area.remove_plane_settings()
        elif self.dock_type == Docks.ProjectionXZ:
            self.area.remove_projection('XZ')
        elif self.dock_type == Docks.PlanesListDock:
            self.area.remove_planes()
        elif self.dock_type == Docks.HistoryDock:
            self.area.remove_history()
        self.area.app_data.docks.remove(self.dock_type)
        self.area.app_data.handlers.call(AppEvent.DocksChanged)

    def do(self):
        if self.dock_type in self.area.app_data.docks:
            return
        if self.dock_type == Docks.Axonometric:
            self.area.add_axonometric()
        elif self.dock_type == Docks.PlaneSettings:
            self.area.add_plane_settings()
        elif self.dock_type == Docks.ProjectionXZ:
            self.area.add_projection("XZ")
        elif self.dock_type == Docks.PlanesListDock:
            self.area.add_planes_list()
        elif self.dock_type == Docks.HistoryDock:
            self.area.add_history()
        self.area.app_data.docks.add(self.dock_type)
        self.area.app_data.handlers.call(AppEvent.DocksChanged)


class RemoveDockCommand(Command):
    def __init__(self, area: "AeflotFrontDockArea", dock_type: Docks):
        self.dock_type = dock_type
        self.area = area

    def undo(self):
        if self.dock_type in self.area.app_data.docks:
            return
        if self.dock_type == Docks.Axonometric:
            self.area.add_axonometric()
        elif self.dock_type == Docks.PlaneSettings:
            self.area.add_plane_settings()
        elif self.dock_type == Docks.ProjectionXZ:
            self.area.add_projection("XZ")
        elif self.dock_type == Docks.PlanesListDock:
            self.area.add_planes_list()
        elif self.dock_type == Docks.HistoryDock:
            self.area.add_history()
        self.area.app_data.docks.add(self.dock_type)
        self.area.app_data.handlers.call(AppEvent.DocksChanged)

    def do(self):
        if self.dock_type not in self.area.app_data.docks:
            return
        if self.dock_type == Docks.Axonometric:
            self.area.remove_axonometric()
        elif self.dock_type == Docks.PlaneSettings:
            self.area.remove_plane_settings()
        elif self.dock_type == Docks.ProjectionXZ:
            self.area.remove_projection('XZ')
        elif self.dock_type == Docks.PlanesListDock:
            self.area.remove_planes()
        elif self.dock_type == Docks.HistoryDock:
            self.area.remove_history()
        self.area.app_data.docks.remove(self.dock_type)
        self.area.app_data.handlers.call(AppEvent.DocksChanged)


class AeflotFrontDockArea(DockArea):
    def __init__(self, app_data: AppData):
        super().__init__()
        self.axonometric = None
        self.plane_settings = None
        self.projection = None
        self.planes_list = None
        self.history_dock = None

        self.app_data = app_data
        self.history = app_data.history
        self.history.add(AddDockCommand(self, Docks.Axonometric))
        self.history.add(AddDockCommand(self, Docks.PlaneSettings))
        self.history.add(AddDockCommand(self, Docks.ProjectionXZ))

    def add_axonometric(self):
        self.axonometric = AxonometricDock(self.app_data)
        self.addDock(self.axonometric, 'left')

    def remove_axonometric(self):
        self.axonometric.remove()
        self.axonometric = None

    def add_plane_settings(self):
        self.plane_settings = PlaneSettingsDock(self.app_data)
        self.plane_settings.setStretch(1, 1)
        self.addDock(self.plane_settings, 'top')

    def remove_plane_settings(self):
        self.plane_settings.remove()
        self.app_data.plane_settings = None

    def add_projection(self, plane):
        self.projection = ProjectionDock(plane, self.app_data)
        if self.axonometric:
            self.addDock(self.projection, 'right', self.axonometric)
        else:
            self.addDock(self.projection, 'right')

    def remove_projection(self, plane):
        self.projection.remove()
        self.projection = None

    def add_planes_list(self):
        self.planes_list = PlanesListDock(self.app_data)
        self.addDock(self.planes_list, 'right')

    def remove_planes(self):
        self.planes_list.remove()
        self.planes_list = None

    def add_history(self):
        self.history_dock = HistoryDock(self.app_data)
        self.addDock(self.history_dock, 'right')

    def remove_history(self):
        self.history_dock.remove()
        self.history_dock = None

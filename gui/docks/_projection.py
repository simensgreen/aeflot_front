from pyqtgraph import PlotWidget
from pyqtgraph.dockarea import Dock


class ProjectionDock(Dock):
    def __init__(self, plane: str):
        super().__init__(f"Проекция на плоскость {plane}")
        self.widget = PlotWidget()
        self.addWidget(self.widget)

    def remove(self):
        self.deleteLater()

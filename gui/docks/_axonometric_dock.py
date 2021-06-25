from pyqtgraph.dockarea import Dock
from pyqtgraph.opengl import GLViewWidget
from pyqtgraph.opengl import GLMeshItem, MeshData, GLSurfacePlotItem
import numpy as np

from utils import AppData, AppEvent


class AxonometricDock(Dock):
    def __init__(self, app_data: AppData):
        super().__init__("Аксонометрия")
        self.app_data = app_data
        self.handler_id = app_data.handlers.add(self.full_update, AppEvent.ModelChanged)
        self.widget = GLViewWidget()
        self.addWidget(self.widget)

    def add_model(self):
        self.widget.addItem(GLMeshItem(meshdata=MeshData(vertexes=self.app_data.model.vertexes), drawEdges=True))

    def add_plane(self):
        print(self.app_data.model.current_plane_value)
        a = np.array([[self.app_data.model.current_plane_value for _ in range(2)] for _ in range(2)])
        self.widget.addItem(GLSurfacePlotItem(z=a, color=(0, .7, .7, .5), glOptions='translucent'))

    def clear(self):
        self.widget.clear()

    def full_update(self):
        self.clear()
        self.add_model()
        self.add_plane()

    def remove(self):
        self.app_data.handlers.remove(self.handler_id)
        self.deleteLater()

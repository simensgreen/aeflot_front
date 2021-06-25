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
        self.widget.addItem(GLMeshItem(meshdata=MeshData(vertexes=self.app_data.model.vertexes), drawEdges=True, computeNormals=False))

    def add_plane(self):
        min_x, min_y, _, max_x, max_y, _ = self.app_data.model.aabb
        dx, dy = max_x - min_x, max_y - min_y
        min_x, min_y = min_x - dx / 5, min_y - dy / 2
        max_x, max_y = max_x + dx / 5, max_y + dy / 2
        z = self.app_data.model.current_plane_value
        surface_vertexes = np.array((
            ((max_x, max_y, z), (min_x, max_y, z), (min_x, min_y, z)),
            ((max_x, max_y, z), (min_x, min_y, z), (max_x, min_y, z))
        ))
        self.widget.addItem(GLMeshItem(meshdata=MeshData(vertexes=surface_vertexes,
                                                         vertexColors=np.array([(0, .7, .7, .5)] * 6)),
                                       glOptions='translucent'))

    def clear(self):
        self.widget.clear()

    def full_update(self):
        self.clear()
        self.add_model()
        self.add_plane()

    def remove(self):
        self.app_data.handlers.remove(self.handler_id)
        self.deleteLater()

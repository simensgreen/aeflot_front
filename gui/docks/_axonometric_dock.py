from PyQt5.QtGui import QVector3D
from pyqtgraph.dockarea import Dock
from pyqtgraph.opengl import GLViewWidget
from pyqtgraph.opengl import GLMeshItem, MeshData, GLAxisItem
import numpy as np

from utils import AppData, AppEvent


class AxonometricDock(Dock):
    def __init__(self, app_data: AppData):
        super().__init__("Аксонометрия")
        self.app_data = app_data
        self.config = self.app_data.config['axonometric']
        self.handler_id = app_data.handlers.add(self.full_update, AppEvent.ModelChanged)
        self.widget = GLViewWidget(rotationMethod='quaternion')
        self.widget.setCameraPosition(
            pos=QVector3D(*map(float, self.config['startup camera position'].split())),
            distance=self.config.getfloat('startup camera distance'))
        self.widget.orbit(self.config.getfloat('startup camera azimuth'),
                          self.config.getfloat('startup camera elevation'))
        self.addWidget(self.widget)
        self.full_update()

    def add_model(self):
        aabb = self.app_data.model.aabb
        self.widget.setCameraPosition(pos=QVector3D((aabb[3] + aabb[0]) / 2,
                                                    (aabb[4] + aabb[1]) / 2,
                                                    (aabb[5] + aabb[2]) / 2))
        self.widget.addItem(GLMeshItem(meshdata=MeshData(vertexes=self.app_data.model.vertexes),
                                       drawEdges=self.config.getboolean('edges'),
                                       computeNormals=False, smooth=False,
                                       shader=self.config['shader'] if self.config['shader'] else None))

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
                                                         vertexColors=np.array([(.40, .40, .80, .5)] * 6)),
                                       glOptions='translucent', smooth=False))

    def add_axis(self):
        axis = GLAxisItem(glOptions='opaque')
        axis.setSize(x=.7, y=.5, z=1)
        self.widget.addItem(axis)

    def clear(self):
        self.widget.setCameraPosition(pos=QVector3D(0, 0, 0))
        self.widget.clear()

    def full_update(self):
        self.clear()
        self.add_model()
        self.add_plane()
        self.add_axis()

    def remove(self):
        self.app_data.handlers.remove(self.handler_id)
        self.deleteLater()

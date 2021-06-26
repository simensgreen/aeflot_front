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
        config = self.app_data.config['axonometric']
        self.handler_id = app_data.handlers.add(self.full_update, AppEvent.ModelChanged)
        self.widget = GLViewWidget(rotationMethod=config['rotation method'])
        self.widget.setCameraPosition(
            pos=QVector3D(*map(float, config['startup camera position'].split())),
            distance=config.getfloat('startup camera distance'))
        self.widget.orbit(config.getfloat('startup camera azimuth'),
                          config.getfloat('startup camera elevation'))
        self.addWidget(self.widget)
        self.full_update()

    def add_model(self):
        if self.app_data.config['axonometric'].getboolean('automatic center'):
            self.center_camera()
        self.widget.addItem(GLMeshItem(meshdata=MeshData(vertexes=self.app_data.model.vertexes),
                                       drawEdges=self.app_data.config['axonometric'].getboolean('edges'),
                                       computeNormals=False, smooth=False,
                                       shader=self.app_data.config['axonometric']['shader']
                                       if self.app_data.config['axonometric']['shader'] else None))

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
        color = tuple(map(float, self.app_data.config['axonometric']['plane color'].split()))
        self.widget.addItem(GLMeshItem(meshdata=MeshData(vertexes=surface_vertexes,
                                                         vertexColors=np.array([color] * 6)),
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
        if self.app_data.config['axonometric'].getboolean('points'):
            self.add_points()
        if self.app_data.config['axonometric'].getboolean('model'):
            self.add_model()
        if self.app_data.config['axonometric'].getboolean('plane'):
            self.add_plane()
        if self.app_data.config['axonometric'].getboolean('axes'):
            self.add_axis()

    def add_points(self):
        for point in self.app_data.model.current_plane_points:
            self.add_point(*point)

    def add_point(self, x, y, z):
        radius = self.app_data.config['axonometric'].getfloat('points radius')
        if not radius:
            return
        mesh_data = MeshData.sphere(rows=5, cols=10, radius=radius)
        color = tuple(map(float, self.app_data.config['axonometric']['points color'].split()))
        mesh_data.setFaceColors(np.array(([color] * mesh_data.faceCount())))
        mesh = GLMeshItem(meshdata=mesh_data, smooth=False)
        mesh.translate(x, y, z)
        self.widget.addItem(mesh)

    def remove(self):
        self.app_data.handlers.remove(self.handler_id)
        self.deleteLater()

    def center_camera(self):
        aabb = self.app_data.model.aabb
        self.widget.setCameraPosition(pos=QVector3D((aabb[3] + aabb[0]) / 2,
                                                    (aabb[4] + aabb[1]) / 2,
                                                    (aabb[5] + aabb[2]) / 2))

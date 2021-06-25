from pyqtgraph.dockarea import Dock
from pyqtgraph.opengl import GLViewWidget
from pyqtgraph.opengl import GLMeshItem, MeshData

from utils import AppData, AppEvent


class AxonometricDock(Dock):
    def __init__(self, app_data: AppData):
        super().__init__("Аксонометрия")
        self.app_data = app_data
        self.handler_id = app_data.handlers.add(self.update_model, AppEvent.ModelChanged)
        self.widget = GLViewWidget()
        self.addWidget(self.widget)
        self.model_item = None

    def add_model(self):
        self.model_item = self.widget.addItem(GLMeshItem(meshdata=MeshData(vertexes=self.app_data.model.vertexes),
                                                         drawEdges=True))

    def update_model(self):
        self.widget.clear()
        self.add_model()

    def remove(self):
        self.app_data.handlers.remove(self.handler_id)
        self.deleteLater()

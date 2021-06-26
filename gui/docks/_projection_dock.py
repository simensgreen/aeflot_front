from PyQt5.QtCore import QRectF, QPointF, QSizeF
from PyQt5.QtGui import QPicture, QPainter, QPainterPath, QPen
from pyqtgraph import PlotWidget, GraphicsObject, mkBrush
from pyqtgraph.dockarea import Dock

from utils import AppData, AppEvent


class ProjectionDock(Dock):
    def __init__(self, plane: str, app_data: AppData):
        super().__init__(f"Проекция на плоскость {plane}")
        self.app_data = app_data
        self.widget = PlotWidget()
        self.widget.setAspectLocked(True)
        self.widget.setAntialiasing(True)
        self.addWidget(self.widget)

        plot = self.widget.getPlotItem()
        self.projection = ProjectionItem(self.app_data.model.current_plane_points, app_data)
        plot.addItem(self.projection)

        self.app_data.handlers.add(self.update, AppEvent.ModelChanged)

    def update(self):
        self.projection.data = self.app_data.model.current_plane_points

    def remove(self):
        self.deleteLater()


class ProjectionItem(GraphicsObject):
    def __init__(self, data, app_data: AppData, *args):
        super().__init__(*args)
        self.picture = QPicture()
        self.app_data = app_data
        self.data = data

    def update_picture(self):
        if len(self.__data) == 0:
            return
        self.picture = QPicture()
        painter = QPainter(self.picture)

        path = QPainterPath()
        path.moveTo(*self.data[0])
        for i in range(1, len(self.data)):
            x, y = self.data[i]
            path.lineTo(float(x), float(y))
        path.closeSubpath()

        fill_color = self.app_data.config['projections']['fill color']
        if fill_color:
            painter.fillPath(path, mkBrush(fill_color))

        stroke_color = self.app_data.config['projections']['stroke color']
        stroke_width = self.app_data.config['projections'].getfloat('stroke width')
        if stroke_color and stroke_width:
            painter.strokePath(path, QPen(mkBrush(stroke_color), stroke_width))

        points_width = self.app_data.config['projections'].getfloat('points size')
        points_color = self.app_data.config['projections']['points color']
        if points_width and points_color:
            points_size = QSizeF(points_width, points_width)
            points_brush = mkBrush(points_color)
            points_width /= 2
            for point in self.data:
                x, y = point
                painter.fillRect(QRectF(QPointF(x - .01, y - .01), points_size), points_brush)

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, new):
        self.__data = new
        self.update_picture()

    def paint(self, p, *_args):
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QRectF(self.picture.boundingRect())

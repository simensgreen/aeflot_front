from PyQt5.QtCore import QRectF, QPointF, QSizeF, Qt
from PyQt5.QtGui import QPicture, QPainter, QPainterPath, QPen, QPolygonF
from pyqtgraph import PlotWidget, GraphicsObject, mkBrush, PlotItem
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

        self.plot: PlotItem = self.widget.getPlotItem()
        if self.app_data.config['projections'].getboolean('use convex hull'):
            points = self.app_data.model.convex_hull_plane_projection
        else:
            points = self.app_data.model.current_plane_projection
        self.projection = ProjectionItem(points, app_data)
        self.plot.addItem(self.projection)

        self.app_data.handlers.add(self.update, AppEvent.ModelChanged)

    def update(self):
        if self.app_data.config['projections'].getboolean('use convex hull'):
            self.projection.data = self.app_data.model.convex_hull_plane_projection
        else:
            self.projection.data = self.app_data.model.current_plane_projection
        self.plot.replot()

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
        path.addPolygon(QPolygonF((QPointF(*point) for point in self.data)))
        path.setFillRule(Qt.WindingFill)
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

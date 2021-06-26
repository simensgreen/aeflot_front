import numpy as np
from dataclasses import dataclass

import open3d

from core.find_coords_point import find_intersections_section
from scipy.spatial import ConvexHull


@dataclass(frozen=True)
class Plane:
    vertices: np.ndarray
    value: float


class Model:
    def __init__(self):
        self.vertices = np.array(())
        self.planes = {}
        self.current_plane_value = 0.0
        self.filename = None

    def load_model(self, filename: str):
        self.filename = filename
        mesh = open3d.io.read_triangle_mesh(filename)
        self.vertices = np.array(tuple(mesh.vertices))

    def unload_model(self):
        self.vertices = np.array(())

    def scale(self, factor_x, factor_y, factor_z):
        for vertex in self.vertices:
            vertex[0] *= factor_x
            vertex[1] *= factor_y
            vertex[2] *= factor_z

    def absolute(self):
        if len(self.vertices) != 0:
            min_x = min(vertex[0] for vertex in self.vertices)
            min_y = min(vertex[1] for vertex in self.vertices)
            min_z = min(vertex[2] for vertex in self.vertices)
            self.move(-min_x, -min_y, -min_z)

    def normalize(self):
        if len(self.vertices) != 0:
            self.absolute()
            factor = 1 / max(abs(value) for vertex in self.vertices for value in vertex)
            self.scale(factor, factor, factor)
            return factor

    def move(self, dx, dy, dz):
        vector = np.array((dx, dy, dz))
        for vertex in self.vertices:
            vertex += vector

    def rotate_x(self, radians):
        matrix = self.rotation_x(radians)
        for i in range(len(self.vertices)):
            self.vertices[i] = matrix @ self.vertices[i]

    def rotate_y(self, radians):
        matrix = self.rotation_y(radians)
        for i in range(len(self.vertices)):
            self.vertices[i] = matrix @ self.vertices[i]

    def rotate_z(self, radians):
        matrix = self.rotation_z(radians)
        for i in range(len(self.vertices)):
            self.vertices[i] = matrix @ self.vertices[i]

    def add_plane(self, x):
        self.planes[x] = Plane(np.array(()), x)

    def remove_plane(self, x):
        if x in self.planes:
            self.planes.pop(x)

    @property
    def vertexes(self):
        shape = self.vertices.shape
        return self.vertices.reshape((shape[0] // 3, 3, 3))

    @property
    def sections(self):
        return tuple((tuple(triangle[i]), tuple(triangle[(i + 1) % 3])) for triangle in self.vertexes for i in range(3))

    @property
    def current_plane_projection(self):
        if self.model_loaded:
            return [(point[0], point[1]) for point in self.current_plane_points]
        else:
            return []

    @staticmethod
    def rotation_x(radians):
        return np.array(((1, 0, 0), (0, np.cos(radians), -np.sin(radians)), (0, np.sin(radians), np.cos(radians))))

    @staticmethod
    def rotation_y(radians):
        return np.array(((np.cos(radians), 0, np.sin(radians)), (0, 1, 0), (-np.sin(radians), 0, np.cos(radians))))

    @staticmethod
    def rotation_z(radians):
        return np.array(((np.cos(radians), -np.sin(radians), 0), (np.sin(radians), np.cos(radians), 0), (0, 0, 1)))

    @property
    def current_plane_points(self):
        if self.model_loaded:
            return find_intersections_section(self.sections, self.current_plane_value)
        else:
            return []

    @property
    def convex_hull_plane_projection(self):
        if self.model_loaded:
            hull = ConvexHull(self.current_plane_projection)
            return [hull.points[i] for i in hull.vertices]
        else:
            return []

    @property
    def model_loaded(self):
        return len(self.vertices) != 0

    @property
    def aabb(self):
        if self.model_loaded:
            min_x = max_x = self.vertices[0][0]
            min_y = max_y = self.vertices[0][1]
            min_z = max_z = self.vertices[0][2]
            for vertex in self.vertices:
                min_x = min(min_x, vertex[0])
                min_y = min(min_y, vertex[1])
                min_z = min(min_z, vertex[2])
                max_z = max(max_z, vertex[2])
                max_y = max(max_y, vertex[1])
                max_x = max(max_x, vertex[0])
            return min_x, min_y, min_z, max_x, max_y, max_z
        else:
            return 0, 0, 0, 0, 0, 0

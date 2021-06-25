import numpy as np
from dataclasses import dataclass

import open3d


@dataclass(frozen=True)
class Plane:
    vertices: np.ndarray
    value: float


class Model:
    def __init__(self):
        self.vertices = np.array(())
        self.planes = {}
        self.current_plane_value = 0.0

    def load_model(self, filename: str):
        mesh = open3d.io.read_triangle_mesh(filename)
        self.vertices = np.array(tuple(mesh.vertices))

    def unload_model(self):
        self.vertices = np.array(())

    def scale(self, factor_x, factor_y, factor_z):
        for vertex in self.vertices:
            vertex[0] *= factor_x
            vertex[1] *= factor_y
            vertex[2] *= factor_z

    def normalize(self):
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

    @staticmethod
    def rotation_x(radians):
        return np.array(((1, 0, 0), (0, np.cos(radians), -np.sin(radians)), (0, np.sin(radians), np.cos(radians))))

    @staticmethod
    def rotation_y(radians):
        return np.array(((np.cos(radians), 0, np.sin(radians)), (0, 1, 0), (-np.sin(radians), 0, np.cos(radians))))

    @staticmethod
    def rotation_z(radians):
        return np.array(((np.cos(radians), -np.sin(radians), 0), (np.sin(radians), np.cos(radians), 0), (0, 0, 1)))

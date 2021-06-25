import numpy as np

from utils import Command, AppData, AppEvent


class AddPlaneCommand(Command):
    def __init__(self, app_data: AppData, x: float):
        self.app_data = app_data
        self.x = x

    def do(self):
        self.app_data.model.add_plane(self.x)
        self.app_data.handlers.call(AppEvent.PlanesChanged)

    def undo(self):
        self.app_data.model.remove_plane(self.x)
        self.app_data.handlers.call(AppEvent.PlanesChanged)


class LoadModelCommand(Command):
    def __init__(self, filename: str, app_data: AppData):
        self.app_data = app_data
        self.filename = filename

    def do(self):
        self.app_data.model.load_model(self.filename)
        self.app_data.handlers.call(AppEvent.ModelChanged)

    def undo(self):
        self.app_data.model.unload_model()
        self.app_data.handlers.call(AppEvent.ModelChanged)


class ScaleModelCommand(Command):
    def __init__(self, scale, app_data: AppData):
        self.app_data = app_data
        self.scale = np.array(scale)

    def do(self):
        self.app_data.model.scale(*self.scale)
        self.app_data.handlers.call(AppEvent.ModelChanged)

    def undo(self):
        self.app_data.model.scale(*(1 / self.scale))
        self.app_data.handlers.call(AppEvent.ModelChanged)


class NormalizeModelCommand(Command):
    def __init__(self, app_data: AppData):
        self.app_data = app_data
        self.factor = 1

    def do(self):
        self.factor = self.app_data.model.normalize()
        self.app_data.handlers.call(AppEvent.ModelChanged)

    def undo(self):
        factor = 1 / self.factor
        self.app_data.model.scale(factor, factor, factor)
        self.app_data.handlers.call(AppEvent.ModelChanged)


class MoveModelCommand(Command):
    def __init__(self, vector: np.ndarray, app_data: AppData):
        self.app_data = app_data
        self.vector = vector

    def do(self):
        self.app_data.model.move(*self.vector)
        self.app_data.handlers.call(AppEvent.ModelChanged)

    def undo(self):
        self.app_data.model.move(*(-self.vector))
        self.app_data.handlers.call(AppEvent.ModelChanged)


class RotateModelXCommand(Command):
    def __init__(self, radians, app_data: AppData):
        self.app_data = app_data
        self.radians = radians

    def do(self):
        self.app_data.model.rotate_x(self.radians)
        self.app_data.handlers.call(AppEvent.ModelChanged)

    def undo(self):
        self.app_data.model.rotate_x(-self.radians)
        self.app_data.handlers.call(AppEvent.ModelChanged)


class RotateModelYCommand(Command):
    def __init__(self, radians, app_data: AppData):
        self.app_data = app_data
        self.radians = radians

    def do(self):
        self.app_data.model.rotate_x(self.radians)
        self.app_data.handlers.call(AppEvent.ModelChanged)

    def undo(self):
        self.app_data.model.rotate_x(-self.radians)
        self.app_data.handlers.call(AppEvent.ModelChanged)


class RotateModelZCommand(Command):
    def __init__(self, radians, app_data: AppData):
        self.app_data = app_data
        self.radians = radians

    def do(self):
        self.app_data.model.rotate_x(self.radians)
        self.app_data.handlers.call(AppEvent.ModelChanged)

    def undo(self):
        self.app_data.model.rotate_x(-self.radians)
        self.app_data.handlers.call(AppEvent.ModelChanged)

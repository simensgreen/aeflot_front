from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QMenuBar, QFileDialog, QInputDialog

from core.model_commands import LoadModelCommand, NormalizeModelCommand, ScaleModelCommand, RotateModelZCommand, \
    RotateModelXCommand, RotateModelYCommand, MoveModelCommand
from gui.widgets.menu_bar.docks_menu import DocksMenu
from gui.widgets.menu_bar.multiline_dialog import MultilineDialog
from utils import AppData, Command, AppEvent

import numpy as np


class SetLoggingFileNameCommand(Command):
    def __init__(self, old, new, app_data: AppData):
        self.old = old
        self.new = new
        self.app_data = app_data

    def do(self):
        self.app_data.config['logging']['filename'] = self.new
        self.app_data.logger.update_config()

    def undo(self):
        self.app_data.config['logging']['filename'] = self.old
        self.app_data.logger.update_config()


class AeflotFrontMenuBar(QMenuBar):
    def __init__(self, app_data: AppData, dock_area):
        super().__init__()
        self.app_data = app_data
        self.history = app_data.history
        self.add_file_menu(self.addMenu("Файл"))
        self.add_model_menu(self.addMenu("Модель"))
        self.docks_menu = DocksMenu(self.app_data, dock_area)
        self.addMenu(self.docks_menu)
        # self.add_docks_menu(self.addMenu("Доки"))
        self.add_app_menu(self.addMenu("Приложение"))
        help_action = self.addAction('Справка')
        help_action.setShortcut("F1")
        help_action.triggered.connect(lambda: print("справка"))

    def add_model_menu(self, menu):
        open_model = menu.addAction("Открыть")
        open_model.setShortcut("Ctrl+O")
        open_model.triggered.connect(self.load_model)
        menu.addSeparator()
        normalize_model = menu.addAction("Нормализовать")
        normalize_model.setShortcut("Ctrl+N")
        normalize_model.triggered.connect(self.normalize_model)
        scale_model = menu.addAction("Масштабировать")
        scale_model.triggered.connect(self.scale_model)
        scale_model.setShortcut("Ctrl+S")
        move_model = menu.addAction("Переместить")
        move_model.triggered.connect(self.move_model)
        move_model.setShortcut("Ctrl+M")
        rotate_menu = menu.addMenu("Вращать")
        rotate_x = rotate_menu.addAction("Вокруг OX")
        rotate_x.triggered.connect(self.rotate_x)
        rotate_y = rotate_menu.addAction("Вокруг OY")
        rotate_y.triggered.connect(self.rotate_y)
        rotate_z = rotate_menu.addAction("Вокруг OZ")
        rotate_z.triggered.connect(self.rotate_z)

    def add_file_menu(self, menu):
        open_model = menu.addAction("Открыть модель")
        open_model.triggered.connect(self.load_model)
        menu.addSeparator()
        undo_action = menu.addAction("Отмена")
        undo_action.setShortcut("Ctrl+Z")
        undo_action.triggered.connect(self.history.cancel_last)
        save_config_action = menu.addAction("Сохранить настройки")
        save_config_action.triggered.connect(self.save_config)

    def add_app_menu(self, menu):
        self.add_settings_menu(menu.addMenu("Настройки"))
        about_action = menu.addAction('Информация')
        about_action.setDisabled(True)
        menu.addSeparator()
        exit_action = menu.addAction("Выход")
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(lambda: self.app_data.handlers.call(AppEvent.ExitApp))

    def add_settings_menu(self, menu):
        logging_menu = menu.addMenu("Журналирование")
        # logging_menu.setDisabled(True)
        logging_file_action = logging_menu.addAction("Имя файла")
        logging_file_action.triggered.connect(self.set_logging_filename)
        logging_level = logging_menu.addMenu("Уровень")
        logging_level.addAction('DEBUG')
        logging_level.addAction('Информация')
        logging_level.addAction('Предупреждения')
        logging_level.addAction('Ошибки')

    def load_model(self):
        filename, not_cancel = QFileDialog.getOpenFileName(self, 'Открыть модель', '', filter='*.stl *.obj')
        if not_cancel:
            self.app_data.history.add(LoadModelCommand(filename, self.app_data))
            if self.app_data.config['model'].getboolean("normalize on load"):
                self.app_data.history.add(NormalizeModelCommand(self.app_data))

    def set_logging_filename(self):
        old_filename = self.app_data.config['logging']['filename']
        new_filename, not_cancel = QInputDialog.getText(self, "Имя файла журнала",
                                                        f'Оставьте пустым чтобы выключить. '
                                                        f'Текущее значение: "{old_filename}"')
        if new_filename != old_filename and not_cancel:
            self.history.add(SetLoggingFileNameCommand(old_filename, new_filename, self.app_data))

    def set_logging_filemode(self):
        old_filemode = self.app_data.config['logging']['filemode']
        new_filename = QInputDialog.getText(self, "Режим открытия файла журнала",
                                            f'Текущее значение: "{old_filemode}". \n"a" - дозапись\n"w"-перезапись')[0]

    def save_config(self):
        with open('config.ini', 'w') as file:
            self.app_data.config.write(file)
            self.app_data.logger.info(f"Настройки сохранены в {file.name}")

    def normalize_model(self):
        self.history.add(NormalizeModelCommand(self.app_data))

    def scale_model(self):
        validator = QRegExpValidator(QRegExp(r"\-?\d*\.?\d*"))
        dialog = MultilineDialog("Масштабирование",
                                 {'name': 'x', 'default': '1.0', 'validator': validator},
                                 {'name': 'y', 'default': '1.0', 'validator': validator},
                                 {'name': 'z', 'default': '1.0', 'validator': validator},
                                 ok='Масштабировать'
                                 )
        dialog.exec()
        x, y, z = dialog.entries['x'].text(), dialog.entries['y'].text(), dialog.entries['z'].text()
        x = float(x) if x else 1.0
        y = float(y) if y else 1.0
        z = float(z) if z else 1.0
        if not dialog.cancelled and any((x != 1.0, y != 1.0, z != 1.0)):
            self.history.add(ScaleModelCommand((x, y, z), self.app_data))

    @staticmethod
    def __rotation_dialog(axis):
        def change_rad(value):
            dialog.entries['Радианы'].setText(str(np.radians(float(value if value else 0))))

        def change_deg(value):
            dialog.entries['Градусы'].setText(str(np.degrees(float(value if value else 0))))

        validator = QRegExpValidator(QRegExp(r"\-?\d*\.?\d*"))
        dialog = MultilineDialog(f'{axis} вращение',
                                 {'name': 'Градусы', 'default': '0.0', 'validator': validator},
                                 {'name': 'Радианы', 'default': '0.0', 'validator': validator},
                                 ok='Вращать')
        dialog.entries['Градусы'].textEdited.connect(change_rad)
        dialog.entries['Радианы'].textEdited.connect(change_deg)
        dialog.exec()
        result = dialog.entries['Радианы'].text()
        return float(result if result else 0.0), dialog.cancelled

    def rotate_x(self):
        result = self.__rotation_dialog("OX")
        if result[0] and not result[1]:
            self.history.add(RotateModelXCommand(result[0], self.app_data))

    def rotate_y(self):
        result = self.__rotation_dialog("OY")
        if result[0] and not result[1]:
            self.history.add(RotateModelYCommand(result[0], self.app_data))

    def rotate_z(self):
        result = self.__rotation_dialog("OZ")
        if result[0] and not result[1]:
            self.history.add(RotateModelZCommand(result[0], self.app_data))

    def move_model(self):
        validator = QRegExpValidator(QRegExp(r"\-?\d*\.?\d*"))
        dialog = MultilineDialog('Перемещение',
                                 {'name': 'dx', 'default': '0.0', 'validator': validator},
                                 {'name': 'dy', 'default': '0.0', 'validator': validator},
                                 {'name': 'dz', 'default': '0.0', 'validator': validator},
                                 ok='Переместить'
                                 )
        dialog.exec()
        dx, dy, dz = dialog.entries['dx'].text(), dialog.entries['dy'].text(), dialog.entries['dz'].text()
        vector = float(dx) if dx else 0, float(dy) if dy else 0, float(dz) if dz else 0
        if not dialog.cancelled and any(vector):
            self.history.add(MoveModelCommand(np.array(vector), self.app_data))

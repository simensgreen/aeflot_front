from PyQt5.QtWidgets import QMenuBar, QFileDialog, QInputDialog,\
    QWidget, QDialog, QVBoxLayout, QLineEdit, QLabel, QHBoxLayout

from core.model_commands import LoadModelCommand, NormalizeModelCommand, ScaleModelCommand
from utils import AppData, Command, AppEvent


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
    def __init__(self, app_data: AppData):
        super().__init__()
        self.app_data = app_data
        self.history = app_data.history
        self.add_file_menu(self.addMenu("Файл"))
        self.add_model_menu(self.addMenu("Модель"))
        self.add_docks_menu(self.addMenu("Доки"))
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
        normalize_model.triggered.connect(self.normalize_model)
        scale_model = menu.addAction("Масштабировать")
        scale_model.triggered.connect(self.scale_model)
        move_model = menu.addAction("Передвинуть")
        rotate_menu = menu.addMenu("Вращать")
        rotate_x = rotate_menu.addAction("Вокруг OX")
        rotate_x.triggered.connect(self.rotate_x)
        rotate_y = rotate_menu.addAction("Вокруг OY")
        rotate_z = rotate_menu.addAction("Вокруг OZ")

    def add_file_menu(self, menu):
        open_model = menu.addAction("Открыть модель")
        open_model.triggered.connect(self.load_model)
        menu.addSeparator()
        undo_action = menu.addAction("Отмена")
        undo_action.setShortcut("Ctrl+Z")
        undo_action.triggered.connect(self.history.cancel_last)
        save_config_action = menu.addAction("Сохранить настройки")
        save_config_action.triggered.connect(self.save_config)

    def add_docks_menu(self, menu):
        axonometric = menu.addAction("Аксонометрия")
        axonometric.setCheckable(True)

        planes = menu.addAction("Плоскости")
        planes.setCheckable(True)

        planes_sets = menu.addAction("Настройки плоскости")
        planes_sets.setCheckable(True)

        projection_xz = menu.addAction("Проекция на плоскость XZ")
        projection_xz.setCheckable(True)

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
        logging_menu.setDisabled(True)
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
        factor, not_cancel = QInputDialog.getDouble(self, "Масштабирование", 'Пока доступен только один множитель')
        if not_cancel:
            self.history.add(ScaleModelCommand((factor, factor, factor), self.app_data))

    def rotate_x(self):
        line_edit_deg = QLineEdit()
        line_edit_deg.textEdited.connect(lambda val: val)

        line_edit_radian = QLineEdit()

        dialog = QDialog(self)
        dialog.setWindowTitle("Вращение вокруг OX")

        vertical_layout = QVBoxLayout()
        horizontal_layout = QHBoxLayout()

        vertical_layout.addWidget(QLabel("Введите угол:"))

        vertical_layout.addLayout(horizontal_layout)

        horizontal_layout.addWidget(QLabel("В градусах"))
        horizontal_layout.addWidget(line_edit_deg)

        horizontal_layout = QHBoxLayout()
        vertical_layout.addLayout(horizontal_layout)

        horizontal_layout.addWidget(QLabel("В радианах"))
        horizontal_layout.addWidget(line_edit_radian)

        dialog.setLayout(vertical_layout)

        dialog.exec()

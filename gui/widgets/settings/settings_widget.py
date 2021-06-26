from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QIntValidator, QRegExpValidator
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QTabWidget, \
    QSpacerItem, QSizePolicy, QCheckBox, QLabel, QLineEdit, QFileDialog, QComboBox
from pyqtgraph import ColorButton

from utils import AppData, DEFAULT_CONFIG, AppEvent
import copy


SHADERS = ['', 'balloon', 'normalColor', 'viewNormalColor', 'shaded', 'edgeHilight', 'heightColor']


class AeflotFrontSettingsWidget(QWidget):
    def __init__(self, app_data: AppData):
        super().__init__()
        self.setWindowFlags(Qt.Tool)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.app_data = app_data
        self.tabs = None

    def show(self):
        self.setWindowTitle('Настройки')
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        self.tabs = QTabWidget()
        main_layout.addWidget(QLabel(text="Если это возможно, настройки применяются сразу, "
                                          "иначе - после сохранения и перезапуска"))
        main_layout.addWidget(self.tabs)
        buttons_layout = QHBoxLayout()
        main_layout.addLayout(buttons_layout)
        vertical_spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        buttons_layout.addItem(vertical_spacer)

        # accept_btn = QPushButton(text='Применить')
        # buttons_layout.addWidget(accept_btn)
        # accept_btn.setFixedWidth(120)

        restore_btn = QPushButton(text='Восстановить')
        buttons_layout.addWidget(restore_btn)
        restore_btn.setFixedWidth(120)
        restore_btn.clicked.connect(self.restore)

        save_btn = QPushButton(text='Сохранить')
        buttons_layout.addWidget(save_btn)
        save_btn.setFixedWidth(120)
        save_btn.clicked.connect(self.save_config)

        # cancel_btn = QPushButton(text='Отменить')
        # buttons_layout.addWidget(cancel_btn)
        # cancel_btn.setFixedWidth(120)

        self.tabs.addTab(WindowSettings(self.app_data), 'Окно')
        self.tabs.addTab(ModelSettings(self.app_data), 'Модель')
        self.tabs.addTab(AxonometricSettings(self.app_data), "Аксонометрия")
        self.tabs.addTab(ProjectionsSettings(self.app_data), "Проекции")
        super().show()

    def save_config(self):
        with open('config.ini', 'w') as file:
            self.app_data.config.write(file)
        self.app_data.logger.info("Настройки сохранены в config.ini")

    def restore(self):
        self.app_data.config = copy.deepcopy(DEFAULT_CONFIG)
        for event in AppEvent:
            if event != AppEvent.ExitApp:
                self.app_data.handlers.call(event)
        self.app_data.logger.info("Настройки восстановлены")
        self.close()


class SettingsWidget(QWidget):
    def __init__(self, app_data: AppData):
        super().__init__()
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.app_data = app_data
        self.float_validator = QRegExpValidator(QRegExp(r"\-?\d*\.?\d*"))

    def add_label_entry(self, text: str):
        layout = QHBoxLayout()
        self.main_layout.addLayout(layout)
        layout.addWidget(QLabel(text=text))
        entry = QLineEdit()
        entry.setFixedWidth(120)
        layout.addWidget(entry)
        return entry

    def add_label_color_btn(self, text, color):
        layout = QHBoxLayout()
        self.main_layout.addLayout(layout)
        layout.addWidget(QLabel(text=text))
        color_btn = ColorButton(self, color)
        layout.addWidget(color_btn)
        return color_btn


class ModelSettings(SettingsWidget):
    def __init__(self, app_data):
        super().__init__(app_data)

        layout = QHBoxLayout()
        self.main_layout.addLayout(layout)

        startup_load_check = QCheckBox(text="Открывать при запуске")
        startup_load_check.setChecked(bool(self.app_data.config['model']['startup model']))
        startup_load_check.clicked.connect(self.switch_startup_path)
        layout.addWidget(startup_load_check)
        self.startup_path = QLineEdit()
        layout.addWidget(self.startup_path)
        self.startup_path.setEnabled(startup_load_check.isChecked())
        self.startup_path.setFixedWidth(300)
        self.startup_path.setText(self.app_data.config['model']['startup model'])

        norm_on_load = QCheckBox(text="Нормализовывать при открытии")
        norm_on_load.setChecked(self.app_data.config['model'].getboolean("normalize on load"))
        norm_on_load.clicked.connect(lambda val:
                                     self.app_data.config['model'].__setitem__('normalize on load', str(val)))
        self.main_layout.addWidget(norm_on_load)

        self.main_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def switch_startup_path(self, value):
        if value:
            self.startup_path.setEnabled(True)
            filename = QFileDialog.getOpenFileName(self, 'Открыть модель', '',
                                                   filter=self.app_data.config['model']['model formats'])[0]
            if filename:
                self.startup_path.setText(filename)
                self.app_data.config['model']['startup model'] = filename
        else:
            self.startup_path.clear()
            self.startup_path.setDisabled(True)
            self.app_data.config['model']['startup model'] = ''


class WindowSettings(SettingsWidget):
    def __init__(self, app_data):
        super().__init__(app_data)

        title = self.add_label_entry("Заголовок")
        title.setText(self.app_data.config['window']['title'])
        title.textChanged.connect(lambda val: self.app_data.config['window'].__setitem__('title', val))

        x_position = self.add_label_entry("Положение по горизонтали")
        x_position.setValidator(QIntValidator())
        x_position.setText(self.app_data.config['window']['x'])
        x_position.textChanged.connect(lambda val: self.app_data.config['window'].__setitem__('x', val))

        y_position = self.add_label_entry("Положение по вертикали")
        y_position.setValidator(QIntValidator())
        y_position.setText(self.app_data.config['window']['y'])
        y_position.textChanged.connect(lambda val: self.app_data.config['window'].__setitem__('y', val))

        width = self.add_label_entry("Ширина")
        width.setText(self.app_data.config['window']['width'])
        width.setValidator(QIntValidator())
        width.textChanged.connect(lambda val: self.app_data.config['window'].__setitem__('width', val))

        height = self.add_label_entry("Высота")
        height.setValidator(QIntValidator())
        height.setText(self.app_data.config['window']['height'])
        height.textChanged.connect(lambda val: self.app_data.config['window'].__setitem__('height', val))

        self.main_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))


class AxonometricSettings(SettingsWidget):
    def __init__(self, app_data: AppData):
        super().__init__(app_data)
        config = self.app_data.config['axonometric']

        startup_cam_distance = self.add_label_entry("Расстояние до камеры при запуске")
        startup_cam_distance.setValidator(self.float_validator)
        startup_cam_distance.setText(config['startup camera distance'])
        startup_cam_distance.textChanged.connect(lambda val: config.__setitem__('startup camera distance', val))

        startup_cam_azimuth = self.add_label_entry("Азимут камеры при запуске")
        startup_cam_azimuth.setValidator(self.float_validator)
        startup_cam_azimuth.setText(config['startup camera azimuth'])
        startup_cam_azimuth.textChanged.connect(lambda val: config.__setitem__('startup camera azimuth', val))

        startup_cam_elevation = self.add_label_entry("Высота камеры при запуске")
        startup_cam_elevation.setValidator(self.float_validator)
        startup_cam_elevation.setText(config['startup camera elevation'])
        startup_cam_elevation.textChanged.connect(lambda val: config.__setitem__('startup camera elevation', val))

        points_radius = self.add_label_entry("Радиус точек")
        points_radius.setValidator(self.float_validator)
        points_radius.setText(config['points radius'])
        points_radius.textChanged.connect(self.change_points_radius)

        plane_color_btn = self.add_label_color_btn('Цвет плоскости сечения',
                                                   tuple(map(lambda val: round(float(val) * 255),
                                                             config['plane color'].split())))
        plane_color_btn.sigColorChanged.connect(self.change_color)

        points_color_btn = self.add_label_color_btn('Цвет точек',
                                                    tuple(map(lambda val: round(float(val) * 255),
                                                              config['points color'].split())))
        points_color_btn.sigColorChanged.connect(self.change_points_color)

        shader_layout = QHBoxLayout()
        self.main_layout.addLayout(shader_layout)
        shader_layout.addWidget(QLabel(text='Шейдер'))
        shader_combobox = QComboBox()
        shader_combobox.addItems(SHADERS)
        shader_combobox.setCurrentText(config['shader'])
        shader_combobox.currentIndexChanged.connect(self.change_shader)
        shader_layout.addWidget(shader_combobox)

        axes = QCheckBox(text='Показывать оси')
        self.main_layout.addWidget(axes)
        axes.setChecked(config.getboolean('axes'))
        axes.clicked.connect(self.check_axes)

        edges = QCheckBox(text='Показывать грани')
        self.main_layout.addWidget(edges)
        edges.setChecked(config.getboolean("edges"))
        edges.clicked.connect(self.check_edges)

        plane = QCheckBox(text='Показывать плоскость')
        self.main_layout.addWidget(plane)
        plane.setChecked(config.getboolean("plane"))
        plane.clicked.connect(self.check_plane)

        model = QCheckBox(text='Показывать модель')
        self.main_layout.addWidget(model)
        model.setChecked(config.getboolean("model"))
        model.clicked.connect(self.check_model)

        points = QCheckBox(text='Показывать точки')
        self.main_layout.addWidget(points)
        points.setChecked(config.getboolean("points"))
        points.clicked.connect(self.check_points)

        auto_center = QCheckBox(text="Центровать камеру")
        self.main_layout.addWidget(auto_center)
        auto_center.setChecked(config.getboolean("automatic center"))
        auto_center.clicked.connect(lambda val:
                                    self.app_data.config['axonometric'].__setitem__("automatic center", str(val)))

        self.main_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def change_points_radius(self, value):
        self.app_data.config['axonometric']['points radius'] = value if value and value != '.' else "0"
        self.app_data.handlers.call(AppEvent.ModelChanged)

    def change_points_color(self, value):
        new_color = value.color('float')
        self.app_data.config['axonometric']['points color'] = ' '.join(map(str, new_color))
        self.app_data.handlers.call(AppEvent.ModelChanged)

    def check_points(self, value):
        self.app_data.config['axonometric']['points'] = str(value)
        self.app_data.handlers.call(AppEvent.ModelChanged)

    def check_axes(self, value):
        self.app_data.config['axonometric']['axes'] = str(value)
        self.app_data.handlers.call(AppEvent.ModelChanged)

    def check_edges(self, value):
        self.app_data.config['axonometric']['edges'] = str(value)
        self.app_data.handlers.call(AppEvent.ModelChanged)

    def check_plane(self, value):
        self.app_data.config['axonometric']['plane'] = str(value)
        self.app_data.handlers.call(AppEvent.ModelChanged)

    def check_model(self, value):
        self.app_data.config['axonometric']['model'] = str(value)
        self.app_data.handlers.call(AppEvent.ModelChanged)

    def change_color(self, value: ColorButton):
        new_color = value.color('float')
        self.app_data.config['axonometric']['plane color'] = ' '.join(map(str, new_color))
        self.app_data.handlers.call(AppEvent.ModelChanged)

    def change_shader(self, value):
        self.app_data.config['axonometric']['shader'] = SHADERS[value]
        self.app_data.handlers.call(AppEvent.ModelChanged)


class ProjectionsSettings(SettingsWidget):
    def __init__(self, app_data: AppData):
        super().__init__(app_data)
        config = self.app_data.config['projections']

        fill_check = QCheckBox(text="Заливка")
        self.main_layout.addWidget(fill_check)
        fill_check.setChecked(bool(config['fill color']))

        stroke_check = QCheckBox(text="Кант")
        self.main_layout.addWidget(stroke_check)
        stroke_check.clicked.connect(self.check_stroke)
        stroke_check.setChecked(bool(config['stroke color'] and config.getfloat('stroke width')))

        point_check = QCheckBox(text="Точки")
        self.main_layout.addWidget(point_check)
        point_check.clicked.connect(self.check_points)
        point_check.setChecked(bool(config['points color'] and config.getfloat('points size')))

        self.stroke_width_entry = self.add_label_entry("Ширина канта")
        self.stroke_width_entry.setText(config['stroke width'])
        self.stroke_width_entry.setValidator(self.float_validator)

        self.point_size_entry = self.add_label_entry("Размер точек")
        self.point_size_entry.setText(config['points size'])
        self.point_size_entry.setValidator(self.float_validator)

        self.fill_color_btn = self.add_label_color_btn("Цвет заливки", config['fill color'])
        self.fill_color_btn.sigColorChanged.connect(self.fill_color)

        stroke_color = config['stroke color'] if config['stroke color'] else '#FFFFFF'
        self.stroke_color_btn = self.add_label_color_btn("Цвет канта", stroke_color)
        self.stroke_color_btn.sigColorChanged.connect(self.stroke_color)

        points_color = config['points color'] if config['points color'] else '#FFFFFF'
        self.point_color_btn = self.add_label_color_btn("Цвет точек", points_color)
        self.point_color_btn.sigColorChanged.connect(self.points_color)

        self.main_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def check_points(self, value):
        self.point_size_entry.setEnabled(value)
        self.app_data.config['projections']['points size'] = DEFAULT_CONFIG['projections']['points size'] \
            if value else str(0)
        self.point_size_entry.setText(self.app_data.config['projections']['points size'])
        self.app_data.handlers.call(AppEvent.ModelChanged)

    def check_stroke(self, value):
        self.stroke_width_entry.setEnabled(value)
        self.app_data.config['projections']['stroke width'] = DEFAULT_CONFIG['projections']['stroke width'] \
            if value else str(0)
        self.stroke_width_entry.setText(self.app_data.config['projections']['stroke width'])
        self.app_data.handlers.call(AppEvent.ModelChanged)

    def check_fill(self, value):
        if value:
            self.app_data.config['projections']['fill color'] = self.fill_color_btn.color().HexRgb
        else:
            self.app_data.config['projections']['fill color'] = ''
        self.app_data.handlers.call(AppEvent.ModelChanged)

    @staticmethod
    def extract_color(value):
        red, green, blue, _ = value.color('byte')
        return "#%2.X%2.X%2.X" % (red, green, blue)

    def fill_color(self, value):
        color = self.extract_color(value)
        self.app_data.config['projections']['fill color'] = color
        self.app_data.handlers.call(AppEvent.ModelChanged)

    def stroke_color(self, value):
        color = self.extract_color(value)
        self.app_data.config['projections']['stroke color'] = color
        self.app_data.handlers.call(AppEvent.ModelChanged)

    def points_color(self, value):
        color = self.extract_color(value)
        self.app_data.config['projections']['points color'] = color
        self.app_data.handlers.call(AppEvent.ModelChanged)

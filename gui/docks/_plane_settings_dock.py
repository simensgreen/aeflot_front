from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSlider, QLineEdit, QPushButton
from pyqtgraph.dockarea import Dock

from core.model_commands import AddPlaneCommand
from utils import AppData, AppEvent


class PlaneSettingsDock(Dock):
    TOLERANCE = 8
    MAX_SCALE = 10 ** TOLERANCE
    __value = 0

    def __init__(self, app_data: AppData):
        super().__init__("Настройки плоскости")
        self.app_data = app_data
        self.log = app_data.logger

        self.widget = QWidget()
        self.addWidget(self.widget)
        main_layout = QVBoxLayout()
        slider_entry = QHBoxLayout()
        main_layout.addLayout(slider_entry)
        self.widget.setLayout(main_layout)
        self.slider = QSlider(orientation=Qt.Horizontal)
        slider_entry.addWidget(self.slider)
        self.entry = QLineEdit()
        self.entry.setValidator(QRegExpValidator(QRegExp(r"0?\.\d*|1\.0")))
        slider_entry.addWidget(self.entry)
        self.add_plane_btn = QPushButton(text='Добавить плоскость')
        self.add_plane_btn.clicked.connect(self.add_plane)
        slider_entry.addWidget(self.add_plane_btn)

        self.slider.setRange(0, self.MAX_SCALE)
        self.slider.valueChanged[int].connect(self.__scale_changed)
        self.entry.textEdited.connect(self.__entry_changed)
        self.entry.setFixedWidth((self.TOLERANCE + 2) * 9)
        self.value = 0.0
        self.update()

    def add_plane(self):
        self.app_data.history.add(AddPlaneCommand(self.app_data, self.value))

    def __update_entry(self):
        self.entry.setText(str(self.value))

    def __update_slider(self):
        self.slider.setValue(round(self.value * self.MAX_SCALE))

    def update(self):
        self.__update_entry()
        self.__update_slider()

    def __scale_changed(self, value: int):
        self.value = value / self.MAX_SCALE
        self.__update_entry()

    def __entry_changed(self, value: str):
        try:
            value = float(value)
        except ValueError:
            value = 0.0
        self.value = value
        self.__update_slider()

    @property
    def value(self) -> float:
        return self.__value

    @value.setter
    def value(self, new: float):
        if not 0.0 <= new <= 1.0:
            self.log.warn(f"Значение должно быть: 0 <= значение <= 1, а не {new}")
            new = min(max(0.0, new), 1.0)
        self.__value = new
        self.app_data.model.current_plane_value = self.value
        self.app_data.handlers.call(AppEvent.ModelChanged)
        self.log.dbg(f"Значение для плоскости изменено на {new}")

    def remove(self):
        self.deleteLater()

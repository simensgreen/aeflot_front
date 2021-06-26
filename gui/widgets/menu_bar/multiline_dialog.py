from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton


class MultilineDialog(QDialog):
    def __init__(self, title, *labels, ok: str = 'Ок', cancel: str = 'Отмена'):
        super().__init__()
        self.cancelled = True
        self.setWindowTitle(title)
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        self.entries = {}

        for label in labels:
            layout = QHBoxLayout()
            main_layout.addLayout(layout)

            text = QLabel(text=label['name'])
            text.setFixedWidth(100)
            layout.addWidget(text)

            entry = QLineEdit()
            self.entries[label['name']] = entry
            layout.addWidget(entry)

            entry.setText(label.get('default', ''))
            entry.setFixedWidth(200)
            if 'validator' in label:
                entry.setValidator(label['validator'])

        buttons = QHBoxLayout()
        main_layout.addLayout(buttons)

        ok_button = QPushButton(text=ok)
        buttons.addWidget(ok_button)
        ok_button.clicked.connect(self.ok)

        cancel_button = QPushButton(text=cancel)
        buttons.addWidget(cancel_button)
        cancel_button.clicked.connect(self.close)

    def ok(self):
        self.cancelled = False
        self.close()

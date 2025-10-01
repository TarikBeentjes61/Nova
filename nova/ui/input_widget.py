from PySide6.QtWidgets import QWidget, QLineEdit, QVBoxLayout
from PySide6.QtCore import Signal

class InputWidget(QWidget):
    input_changed = Signal(str)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        self.input = QLineEdit()
        self.input.textChanged.connect(self.emit_change)
        self.input.width = 800
        layout.addWidget(self.input)
        self.setLayout(layout)

    def emit_change(self):
        text = self.input.text()
        self.input_changed.emit(text)

    def set_input(self, text):
        #dont emit signal
        self.input.blockSignals(True)
        self.input.setText(text)
        self.input.blockSignals(False)

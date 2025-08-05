from PySide6.QtWidgets import QWidget, QLineEdit, QVBoxLayout
from PySide6.QtCore import Signal

class InputWidget(QWidget):
    input_changed = Signal(str)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        self.input = QLineEdit()
        self.input.setPlaceholderText("Type and press Enter...")
        self.input.returnPressed.connect(self.emit_search)  

        layout.addWidget(self.input)
        self.setLayout(layout)

    def emit_search(self):
        text = self.input.text()
        self.input_changed.emit(text)

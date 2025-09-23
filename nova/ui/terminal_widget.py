from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit

class TerminalWidget(QWidget):
    def __init__(self, name: str):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.name = name


        
    def on_stdout(self):
        pass

    def send_input(self, input: str):
        pass
from PySide6.QtWidgets import QWidget, QVBoxLayout
from .terminal_widget import TerminalWidget

class TerminalManagerWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.terminals = {}
        self.active_terminal = None

    def new_terminal(self, name: str):
        terminal = TerminalWidget(name)
        self.terminals[name] = terminal
        self.active_terminal = terminal
        self.layout().addWidget(terminal)

    def get_terminal(self, terminal_name):
        return self.terminals.get(terminal_name, None)
        
    def open_terminal(self, terminal):
        pass

    def close_terminal(self, terminal_name):
        pass
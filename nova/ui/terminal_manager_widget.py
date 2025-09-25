from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget
from .terminal_widget import TerminalWidget

class TerminalManagerWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        self.terminals = {}

        #controls
        self.controls_layout = QHBoxLayout()
        self.buttons = []

        #stacked widget for terminals
        self.stack = QStackedWidget()
        layout.addWidget(self.stack)

        layout.addLayout(self.controls_layout)

    def new_terminal(self, name: str):
        terminal = TerminalWidget(name)
        self.terminals[name] = terminal
        self.active_terminal = terminal

        terminal_button = QPushButton(name)
        terminal_button.clicked.connect(lambda _, t=terminal: self.open_terminal(t))
        self.buttons.append(terminal_button)
        self.controls_layout.addWidget(terminal_button)

        self.stack.addWidget(terminal)
        self.open_terminal(terminal)

    def get_terminal(self, terminal_name):
        return self.terminals.get(terminal_name, None)
        
    def get_active_terminal(self):
        if self.stack.currentWidget():
            return self.stack.currentWidget()
        return None

    def get_terminal_count(self):
        return len(self.terminals)

    def get_available_terminal(self):
        for terminal in self.terminals.values():
            if not terminal.is_busy():
                return terminal
        return False

    def open_terminal(self, terminal):
        self.stack.setCurrentWidget(terminal)

    def close_terminal(self, terminal_name):
        pass
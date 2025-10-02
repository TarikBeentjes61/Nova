from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt, QEvent
from .input_widget import InputWidget
from .suggestions_widget import SuggestionsWidget
from .terminal_manager_widget import TerminalManagerWidget
from nova.service.suggestions_service import SuggestionsService
from nova.service.command_service import CommandService
from nova.core.settings import AppSettings
from nova.model.suggestion import Suggestion, Custom, Cmd, Parameter, Program
import os

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nova")
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        layout = QVBoxLayout()
        self.current_suggestion = None

        #Setup Widgets
        self.input_widget = InputWidget()
        self.suggestions_widget = SuggestionsWidget()
        self.suggestions_widget.suggestions_list.setFocusPolicy(Qt.NoFocus)
        self.terminalManager_widget = TerminalManagerWidget()

        layout.addWidget(self.input_widget)
        layout.addWidget(self.suggestions_widget)
        layout.addWidget(self.terminalManager_widget)
        self.setLayout(layout)

        #Setup Services
        self.suggestions_service = SuggestionsService()
        self.command_service = CommandService(self.terminalManager_widget)

        #Setup settings 
        self.appSettings = AppSettings()
        self.apply_settings()
        self.appSettings.settings_changed.connect(self.apply_settings)

        #Setup events
        self.input_widget.input_changed.connect(self.on_input_changed)
        self.suggestions_widget.suggestion_selected.connect(self.on_suggestion_selected)

    
    def on_input_changed(self, input):
        self.update_suggestions(input)

    #handle completion
    def on_suggestion_selected(self, suggestion):
        input_text = self.input_widget.input.text()
        tokens = input_text.strip().split()

        if isinstance(suggestion, Program):
            new_text = suggestion.name
            self.current_suggestion = suggestion

        elif isinstance(suggestion, Cmd) or isinstance(suggestion, Custom):
            self.current_suggestion = suggestion
            if len(tokens) > 1:
                tokens[0] = suggestion.name
                new_text = " ".join(tokens)
            else:
                new_text = suggestion.name

        elif isinstance(suggestion, Parameter):
            param_text = f"{suggestion.name}"
            has_trailing_space = input_text.endswith(" ")

            if has_trailing_space:
                tokens.append(param_text)
            else:
                if len(tokens) > 1:
                    tokens[-1] = param_text
                else:
                    tokens.append(param_text)

            new_text = " ".join(tokens)

        else:
            new_text = input_text 

        self.update_input(new_text)

    def update_input(self, text):
        self.input_widget.set_input(text)
        self.input_widget.input.setCursorPosition(len(text))
        self.input_widget.input.setFocus()
        self.adjustSize()
        
    def update_suggestions(self, input):
        suggestions, matching_suggestion = self.suggestions_service.get_suggestions(input)

        if matching_suggestion:
            self.current_suggestion = matching_suggestion
        else: 
            self.current_suggestion = None

        if suggestions:
            self.suggestions_widget.update_suggestions(suggestions)
            self.suggestions_widget.show()
            self.adjustSize()
        else:
            self.suggestions_widget.update_suggestions(suggestions)
            self.suggestions_widget.hide()

    def apply_theme(self, theme):
        path = f"nova/resources/{theme}.qss"
        if os.path.exists(path):
            with open(path) as f:
                self.setStyleSheet(f.read())
        else:
            print(f"Theme file not found: {path}")

    def apply_settings(self):
        if self.appSettings == None:
            self.appSettings = AppSettings()
        self.apply_theme(self.appSettings.get("theme"))

    #handle inputs 
    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Tab, Qt.Key_Down):
                self.suggestions_widget.navigate_suggestions(forward=True)
                return True
            elif event.key() in (Qt.Key_Backtab, Qt.Key_Up):
                self.suggestions_widget.navigate_suggestions(forward=False)
                return True
            elif event.key() == Qt.Key_Return:
                command_input = self.input_widget.input.text()
                self.command_service.execute(command_input, self.current_suggestion)
                return True
            elif event.key() == Qt.Key_Escape:
                self.close()
                return True    
        return super().eventFilter(obj, event)
    



        

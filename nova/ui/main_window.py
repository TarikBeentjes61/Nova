from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt, QEvent
from .input_widget import InputWidget
from .suggestions_widget import SuggestionsWidget
from nova.service.suggestions_service import SuggestionsService
from nova.core.settings import AppSettings
import os

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nova")
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        layout = QVBoxLayout()
        self.last_token = None

        #Setup Widgets
        self.input_widget = InputWidget()
        self.suggestions_widget = SuggestionsWidget()
        self.suggestions_widget.suggestions_list.setFocusPolicy(Qt.NoFocus)
        layout.addWidget(self.input_widget)
        layout.addWidget(self.suggestions_widget)
        self.setLayout(layout)

        #Setup Services
        self.suggestions_service = SuggestionsService()

        #Setup settings 
        self.appSettings = AppSettings()
        self.apply_settings()
        self.appSettings.settings_changed.connect(self.apply_settings)

        #Setup events
        self.input_widget.input_changed.connect(self.on_input_changed)
        self.suggestions_widget.suggestion_selected.connect(self.on_suggestion_selected)
        self.appSettings.set("theme", "light")

    def on_input_changed(self, input):
        suggestions = self.suggestions_service.get_suggestions(input)
        self.suggestions_widget.update_suggestions(suggestions)

    #handle completion     
    def on_suggestion_selected(self, suggestion):
        print(f"Suggestion selected: {suggestion}")

        self.adjustSize()

    def update_suggestions(self, input):
        suggestions = self.suggestions_service.get_suggestions(input)
        if suggestions:
            self.suggestions_widget.update_suggestions(suggestions)
            self.suggestions_widget.show()
            self.adjustSize()
        else:
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
            elif event.key() in (Qt.Key_Return, Qt.Key_Enter):
                self.suggestions_widget.select_current_suggestion()
                return True
            elif event.key() == Qt.Key_Escape:
                self.close()
                return True    
    



        

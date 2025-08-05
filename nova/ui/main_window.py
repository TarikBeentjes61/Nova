from PySide6.QtWidgets import QWidget, QVBoxLayout
from .input_widget import InputWidget
from .suggestions_widget import SuggestionsWidget
from nova.service.suggestions_service import SuggestionsService
from nova.core.settings import AppSettings
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nova")
        layout = QVBoxLayout()

        #Setup Widgets
        self.input_widget = InputWidget()
        self.suggestions_widget = SuggestionsWidget()
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
        self.input_widget.input_changed.connect(self.on_search)
        self.appSettings.set("theme", "light")

    def on_search(self, input):
        suggestions = self.suggestions_service.get_suggestions(input)
        self.suggestions_widget.update_suggestions(suggestions)
        
    def apply_theme(self, theme):
        with open(f"nova/resources/{theme}.qss") as f:
            self.setStyleSheet(f.read())

    def apply_settings(self):
        if self.appSettings == None:
            self.appSettings = AppSettings()
        self.apply_theme(self.appSettings.get("theme"))



        

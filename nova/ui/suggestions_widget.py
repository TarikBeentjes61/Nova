from PySide6.QtWidgets import QWidget, QListWidget, QVBoxLayout, QLabel

class SuggestionsWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        self.label = QLabel("Suggestions:")
        self.suggestions_list = QListWidget()

        layout.addWidget(self.label)
        layout.addWidget(self.suggestions_list)
        self.setLayout(layout)

    def update_suggestions(self, items):
        self.suggestions_list.clear()
        self.suggestions_list.addItems(items)

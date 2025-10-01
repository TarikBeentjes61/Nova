from PySide6.QtWidgets import QWidget, QListWidget, QVBoxLayout, QSizePolicy, QListWidgetItem
from PySide6.QtCore import Qt, Signal
from nova.model.command import Parameter
from nova.model.suggestion import Suggestion

class SuggestionsWidget(QWidget):
    suggestion_selected = Signal(object)

    def __init__(self):
        super().__init__()
        #setup list
        self.item_height = 30
        self.maximumItems = 20
        self.suggestions_list = QListWidget()
        self.suggestions_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.suggestions_list.setMaximumHeight(self.item_height)
        self.suggestions_list.setFocusPolicy(Qt.StrongFocus)

        #setup widgets
        layout = QVBoxLayout()
        layout.addStretch()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.suggestions_list)
        self.setLayout(layout)
        
        #setup events
        self.suggestions_list.itemClicked.connect(self.on_item_clicked)

    def update_suggestions(self, items):
        self.suggestions_list.clear()
        if items:
            for item in items:
                if isinstance(item, Suggestion):
                    display_text = item.name
                elif isinstance(item, Parameter):
                    display_text = f"{item.name} - ({item.description})"

                list_item = QListWidgetItem(display_text)
                list_item.setData(Qt.UserRole, item) 
                self.suggestions_list.addItem(list_item)

            row_height = self.suggestions_list.sizeHintForRow(0)
            visible_count = min(len(items), self.maximumItems)
            total_height = row_height * visible_count + 2 * self.suggestions_list.frameWidth()
            self.suggestions_list.setFixedHeight(total_height)
        else:
            self.suggestions_list.setFixedHeight(0)

        self.adjustSize()

    def update_selectedSuggestion(self, input):
        tokens = input.strip().split()
        last_token = tokens[-1] if tokens else None

        if last_token:
            for i in range(self.suggestions_list.count()):
                item = self.suggestions_list.item(i)
                item_text = item.text()
                if item_text.startswith(last_token):
                    self.suggestions_list.setCurrentRow(i)
                    self.suggestions_list.scrollToItem(item)
                    return

    def navigate_suggestions(self, forward=True):
        if self.suggestions_list.count() == 0:
            return
        
        if self.suggestions_list.currentRow():
            current_row = self.suggestions_list.currentRow()
        else:
            current_row = 0
        if forward:
            next_row = current_row + 1 if current_row < self.suggestions_list.count() - 1 else 0
        else:
            next_row = current_row - 1 if current_row > 0 else self.suggestions_list.count() - 1
        
        self.suggestions_list.setCurrentRow(next_row)
        self.suggestions_list.scrollToItem(self.suggestions_list.item(next_row))
        self.suggestion_selected.emit(self.suggestions_list.item(next_row).data(Qt.UserRole))

    def has_suggestions(self):
        return self.suggestions_list.count() > 0
    
    def get_selected_parameter(self):
        current_item = self.suggestions_list.currentItem()
        if current_item:
            data = current_item.data(Qt.UserRole)
            if isinstance(data, Parameter):
                return data
        return None

    def on_item_clicked(self, item):
        self.suggestion_selected.emit(item.data(Qt.UserRole))

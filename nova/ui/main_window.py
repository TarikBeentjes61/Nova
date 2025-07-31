import sys
from PySide6 import QtCore, QtWidgets, QtGui

# Constants for styling and layout
WINDOW_WIDTH = 600
WINDOW_BASE_HEIGHT = 80
WINDOW_RADIUS = 15
SEARCH_BAR_HEIGHT = 52
SEARCH_BAR_FONT_SIZE = 18
SEARCH_BAR_RADIUS = 25

# Suggestions
SUGGESTION_ITEM_HEIGHT = 35
MAX_VISIBLE_SUGGESTIONS = 10
SUGGESTION_LIST_MARGIN = 20

# Colors
COLOR_BACKGROUND = "rgba(10, 10, 10, 220)"
COLOR_SEARCH_BG = "rgba(20, 20, 25, 200)"
COLOR_SEARCH_BORDER = "rgba(60, 60, 70, 150)"
COLOR_SEARCH_HOVER_BG = "rgba(30, 30, 35, 210)"
COLOR_SEARCH_FOCUS_BG = "rgba(25, 25, 30, 230)"
COLOR_TEXT = "#f0f0f0"
COLOR_PLACEHOLDER = "rgba(200, 200, 200, 100)"
COLOR_SUGGESTION_BG = "rgba(15, 15, 20, 220)"
COLOR_SUGGESTION_HOVER = "rgba(40, 40, 50, 180)"
COLOR_SUGGESTION_SELECTED = "rgba(70, 120, 255, 120)"
COLOR_SCROLLBAR_BG = "rgba(30, 30, 35, 180)"
COLOR_SCROLLBAR_HANDLE = "rgba(100, 100, 110, 180)"
COLOR_SCROLLBAR_HANDLE_HOVER = "rgba(130, 130, 140, 200)"


class SuggestionsDisplay(QtWidgets.QWidget):
    suggestion_clicked = QtCore.Signal(str)

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.suggestions_list = QtWidgets.QListWidget()
        self.suggestions_list.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.suggestions_list.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.suggestions_list.setFocusPolicy(QtCore.Qt.NoFocus)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 5, 0, 0)
        layout.addWidget(self.suggestions_list)

        # Connect signals
        self.suggestions_list.itemClicked.connect(self.on_item_clicked)
        self.suggestions_list.itemActivated.connect(self.on_item_clicked)  # Enter key support

    def set_suggestions(self, suggestions, require_input=False):
        self.suggestions_list.clear()
        if require_input:
            msg_item = QtWidgets.QListWidgetItem("⚠ This parameter requires an input")
            msg_item.setFlags(QtCore.Qt.NoItemFlags)
            msg_item.setForeground(QtGui.QColor("orange"))
            self.suggestions_list.addItem(msg_item)
            return

        if not suggestions:
            return
        for suggestion in suggestions:
            self.suggestions_list.addItem(QtWidgets.QListWidgetItem(suggestion))

    def get_suggested_height(self):
        item_count = self.suggestions_list.count()
        if item_count == 0:
            return 0
        if item_count <= MAX_VISIBLE_SUGGESTIONS:
            return item_count * SUGGESTION_ITEM_HEIGHT + SUGGESTION_LIST_MARGIN
        else:
            return MAX_VISIBLE_SUGGESTIONS * SUGGESTION_ITEM_HEIGHT + SUGGESTION_LIST_MARGIN

    @QtCore.Slot(QtWidgets.QListWidgetItem)
    def on_item_clicked(self, item):
        if item.flags() != QtCore.Qt.NoItemFlags:
            self.suggestion_clicked.emit(item.text())


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_styling()

    def setup_ui(self):
        self.setWindowTitle("Nova")
        self.setFixedSize(WINDOW_WIDTH, WINDOW_BASE_HEIGHT)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.drag_position = None
        self.base_height = WINDOW_BASE_HEIGHT
        self.text_changed_callback = None
        self.current_suggestions = []

        self.search_bar = QtWidgets.QLineEdit()
        self.search_bar.setPlaceholderText("Search anything...")
        self.search_bar.setFixedHeight(SEARCH_BAR_HEIGHT)
        self.search_bar.setFocusPolicy(QtCore.Qt.StrongFocus)

        self.suggestions_display = SuggestionsDisplay()
        self.suggestions_display.setVisible(False)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(0)
        layout.addWidget(self.search_bar)
        layout.addWidget(self.suggestions_display)

        self.search_bar.returnPressed.connect(self.handle_search)
        self.search_bar.textChanged.connect(self.handle_text_changed)
        self.suggestions_display.suggestion_clicked.connect(self.on_suggestion_selected)

        # Install event filter for Tab navigation
        self.search_bar.installEventFilter(self)

        self.center_window()

    def setup_styling(self):
        style = f"""
        QWidget {{
            background: {COLOR_BACKGROUND};
            border-radius: {WINDOW_RADIUS}px;
        }}

        QLineEdit {{
            background: {COLOR_SEARCH_BG};
            border: 1px solid {COLOR_SEARCH_BORDER};
            border-radius: {SEARCH_BAR_RADIUS}px;
            padding: 0 25px;
            font-size: {SEARCH_BAR_FONT_SIZE}px;
            font-weight: 400;
            color: {COLOR_TEXT};
            selection-background-color: {COLOR_SUGGESTION_SELECTED};
        }}

        QLineEdit:focus {{
            border: 1px solid {COLOR_SEARCH_BORDER};
            background: {COLOR_SEARCH_FOCUS_BG};
        }}

        QLineEdit:hover {{
            background: {COLOR_SEARCH_HOVER_BG};
            border: 1px solid rgba(80, 80, 90, 180);
        }}

        QLineEdit::placeholder {{
            color: {COLOR_PLACEHOLDER};
            font-style: italic;
        }}

        QListWidget {{
            background: {COLOR_SUGGESTION_BG};
            border: 1px solid {COLOR_SEARCH_BORDER};
            border-radius: 15px;
            padding: 8px;
            font-size: 14px;
            color: #e0e0e0;
            outline: none;
        }}

        QListWidget::item {{
            background: transparent;
            padding: 8px 12px;
            border-radius: 8px;
            margin: 2px 0;
        }}

        QListWidget::item:hover {{
            background: {COLOR_SUGGESTION_HOVER};
        }}

        QListWidget::item:selected {{
            background: {COLOR_SUGGESTION_SELECTED};
        }}

        QScrollBar:vertical {{
            background: {COLOR_SCROLLBAR_BG};
            width: 8px;
            border-radius: 4px;
            margin: 0;
        }}

        QScrollBar::handle:vertical {{
            background: {COLOR_SCROLLBAR_HANDLE};
            border-radius: 4px;
            min-height: 20px;
        }}

        QScrollBar::handle:vertical:hover {{
            background: {COLOR_SCROLLBAR_HANDLE_HOVER};
        }}

        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        """
        self.setStyleSheet(style)

    def center_window(self):
        screen = QtGui.QGuiApplication.primaryScreen().geometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen.center())
        self.move(window_geometry.topLeft())

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        path = QtGui.QPainterPath()
        path.addRoundedRect(self.rect(), WINDOW_RADIUS, WINDOW_RADIUS)

        painter.fillPath(path, QtGui.QColor(8, 8, 12, 240))

        pen1 = QtGui.QPen(QtGui.QColor(60, 60, 70, 120))
        pen1.setWidth(1)
        painter.setPen(pen1)
        painter.drawPath(path)

        inner_path = QtGui.QPainterPath()
        inner_rect = self.rect().adjusted(1, 1, -1, -1)
        inner_path.addRoundedRect(inner_rect, WINDOW_RADIUS - 1, WINDOW_RADIUS - 1)
        pen2 = QtGui.QPen(QtGui.QColor(40, 40, 50, 80))
        pen2.setWidth(1)
        painter.setPen(pen2)
        painter.drawPath(inner_path)

    @QtCore.Slot()
    def handle_search(self):
        suggestions_list = self.suggestions_display.suggestions_list
        selected_item = suggestions_list.currentItem()

        if selected_item and selected_item.flags() != QtCore.Qt.NoItemFlags:
            self.on_suggestion_selected(selected_item.text())
            return

        # Normal search
        search_text = self.search_bar.text().strip()
        if search_text:
            print(f"Searching for: {search_text}")

        QtCore.QTimer.singleShot(0, lambda: (
            self.search_bar.deselect(),
            self.search_bar.setCursorPosition(len(search_text))
        ))

    @QtCore.Slot(str)
    def handle_text_changed(self, text):
        if self.text_changed_callback:
            self.text_changed_callback(text)
        if len(text) == 0:
            self.hide_suggestions()

    def set_text_changed_callback(self, callback):
        self.text_changed_callback = callback

    def set_suggestions(self, suggestions, require_input=False):
        self.current_suggestions = suggestions
        self.suggestions_display.set_suggestions(suggestions, require_input)
        if require_input or suggestions:
            self.show_suggestions()
        else:
            self.hide_suggestions()

    def show_suggestions(self):
        if not self.suggestions_display.isVisible():
            self.suggestions_display.setVisible(True)
            suggestions_height = self.suggestions_display.get_suggested_height()
            new_height = self.base_height + suggestions_height
            self.setFixedSize(WINDOW_WIDTH, new_height)

    def hide_suggestions(self):
        if self.suggestions_display.isVisible():
            self.suggestions_display.setVisible(False)
            self.setFixedSize(WINDOW_WIDTH, self.base_height)

    @QtCore.Slot(str)
    def on_suggestion_selected(self, suggestion):
        current_text = self.search_bar.text().strip()

        if not current_text:
            new_text = suggestion
        else:
            words = current_text.split()
            if suggestion.startswith("-"):
                words.append(suggestion)
            else:
                if current_text.endswith(" "):
                    words.append(suggestion)
                else:
                    words[-1] = suggestion
            new_text = " ".join(words)

        new_text += " "

        self.search_bar.setText(new_text)
        self.search_bar.setCursorPosition(len(new_text))
        self.search_bar.deselect()
        self.search_bar.setFocus()

        if self.text_changed_callback:
            self.text_changed_callback(new_text)

    def move_selection(self, direction):
        suggestions_list = self.suggestions_display.suggestions_list
        count = suggestions_list.count()
        if count == 0:
            return
        current_row = suggestions_list.currentRow()
        if current_row < 0:
            current_row = 0 if direction > 0 else count - 1
        else:
            current_row = (current_row + direction) % count
        # Skip disabled items
        while (suggestions_list.item(current_row).flags() == QtCore.Qt.NoItemFlags):
            current_row = (current_row + direction) % count
        suggestions_list.setCurrentRow(current_row)

    def eventFilter(self, source, event):
        if source == self.search_bar and event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Tab and self.suggestions_display.isVisible():
                self.move_selection(1 if not (event.modifiers() & QtCore.Qt.ShiftModifier) else -1)
                return True
            elif event.key() == QtCore.Qt.Key_Up and self.suggestions_display.isVisible():
                self.move_selection(-1)
                return True
            elif event.key() == QtCore.Qt.Key_Down and self.suggestions_display.isVisible():
                self.move_selection(1)
                return True
        return super().eventFilter(source, event)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            if self.suggestions_display.isVisible():
                self.hide_suggestions()
            else:
                self.close()
        super().keyPressEvent(event)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton and self.drag_position is not None:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.drag_position = None
            event.accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()

    # Example demo:
    def on_text_changed(text):
        if text.strip() == "--flag":
            window.set_suggestions([], require_input=True)
        else:
            suggestions = ["apple", "banana", "cherry", "--flag"]
            filtered = [s for s in suggestions if text.lower() in s.lower()]
            window.set_suggestions(filtered)

    window.set_text_changed_callback(on_text_changed)
    sys.exit(app.exec())

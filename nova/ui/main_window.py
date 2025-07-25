import sys
from PySide6 import QtCore, QtWidgets, QtGui

class SuggestionsDisplay(QtWidgets.QWidget):
    suggestion_clicked = QtCore.Signal(str)
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        # Create suggestions list
        self.suggestions_list = QtWidgets.QListWidget()
        self.suggestions_list.setMaximumHeight(200)
        self.suggestions_list.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.suggestions_list.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        
        # Layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 5, 0, 0)
        layout.addWidget(self.suggestions_list)
        
        # Connect signals
        self.suggestions_list.itemClicked.connect(self.on_item_clicked)
        
    def set_suggestions(self, suggestions):
        """Set the suggestions to display"""
        self.suggestions_list.clear()
        
        if not suggestions:
            return
            
        for suggestion in suggestions:
            item = QtWidgets.QListWidgetItem(suggestion)
            self.suggestions_list.addItem(item)
            
    def get_suggested_height(self):
        """Calculate the height needed for current suggestions"""
        item_count = self.suggestions_list.count()
        if item_count == 0:
            return 0
            
        item_height = 35  # Approximate height per item
        max_visible_items = 6
        
        if item_count <= max_visible_items:
            return item_count * item_height + 20
        else:
            return max_visible_items * item_height + 20
            
    @QtCore.Slot(QtWidgets.QListWidgetItem)
    def on_item_clicked(self, item):
        self.suggestion_clicked.emit(item.text())

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_styling()
        
    def setup_ui(self):
        # Set window properties
        self.setWindowTitle("Nova")
        self.setFixedSize(600, 80)  # Will be resized dynamically
        
        # Make window frameless and always on top
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        # Initialize drag variables
        self.drag_position = None
        self.base_height = 80
        
        # Initialize callback and suggestions
        self.text_changed_callback = None
        self.current_suggestions = []
        
        # Create search bar
        self.search_bar = QtWidgets.QLineEdit()
        self.search_bar.setPlaceholderText("Search anything...")
        self.search_bar.setFixedHeight(52)
        
        # Create suggestions display
        self.suggestions_display = SuggestionsDisplay()
        self.suggestions_display.setVisible(False)
        
        # Create layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(0)
        layout.addWidget(self.search_bar)
        layout.addWidget(self.suggestions_display)
        
        # Connect signals
        self.search_bar.returnPressed.connect(self.handle_search)
        self.search_bar.textChanged.connect(self.handle_text_changed)
        self.suggestions_display.suggestion_clicked.connect(self.on_suggestion_selected)
        
        # Center window on screen
        self.center_window()
        
    def setup_styling(self):
        # Very dark frosted glass theme
        style = """
        QWidget {
            background: rgba(10, 10, 10, 220);
            border-radius: 15px;
        }
        
        QLineEdit {
            background: rgba(20, 20, 25, 200);
            border: 1px solid rgba(60, 60, 70, 150);
            border-radius: 25px;
            padding: 0 25px;
            font-size: 18px;
            font-weight: 400;
            color: #f0f0f0;
            selection-background-color: rgba(70, 120, 255, 120);
        }
        
        QLineEdit:focus {
            border: 2px solid rgba(70, 120, 255, 255);
            background: rgba(25, 25, 30, 230);
            box-shadow: 0 0 20px rgba(70, 120, 255, 50);
        }
        
        QLineEdit:hover {
            background: rgba(30, 30, 35, 210);
            border: 1px solid rgba(80, 80, 90, 180);
        }
        
        QLineEdit::placeholder {
            color: rgba(200, 200, 200, 100);
            font-style: italic;
        }
        
        QListWidget {
            background: rgba(15, 15, 20, 220);
            border: 1px solid rgba(60, 60, 70, 150);
            border-radius: 15px;
            padding: 8px;
            font-size: 14px;
            color: #e0e0e0;
            outline: none;
        }
        
        QListWidget::item {
            background: transparent;
            padding: 8px 12px;
            border-radius: 8px;
            margin: 2px 0;
        }
        
        QListWidget::item:hover {
            background: rgba(40, 40, 50, 180);
        }
        
        QListWidget::item:selected {
            background: rgba(70, 120, 255, 120);
        }
        
        QScrollBar:vertical {
            background: rgba(30, 30, 35, 180);
            width: 8px;
            border-radius: 4px;
            margin: 0;
        }
        
        QScrollBar::handle:vertical {
            background: rgba(100, 100, 110, 180);
            border-radius: 4px;
            min-height: 20px;
        }
        
        QScrollBar::handle:vertical:hover {
            background: rgba(130, 130, 140, 200);
        }
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
        """
        self.setStyleSheet(style)
        
    def center_window(self):
        # Center the window on the screen
        screen = QtGui.QGuiApplication.primaryScreen().geometry()
        window_geometry = self.frameGeometry()
        center_point = screen.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())
        
    def paintEvent(self, event):
        # Create enhanced frosted glass effect
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        
        # Create rounded rectangle path
        path = QtGui.QPainterPath()
        path.addRoundedRect(self.rect(), 15, 15)
        
        # Fill with very dark semi-transparent color for frosted effect
        painter.fillPath(path, QtGui.QColor(8, 8, 12, 240))
        
        # Add multiple subtle borders for depth
        pen1 = QtGui.QPen(QtGui.QColor(60, 60, 70, 120))
        pen1.setWidth(1)
        painter.setPen(pen1)
        painter.drawPath(path)
        
        # Inner glow effect
        inner_path = QtGui.QPainterPath()
        inner_rect = self.rect().adjusted(1, 1, -1, -1)
        inner_path.addRoundedRect(inner_rect, 14, 14)
        pen2 = QtGui.QPen(QtGui.QColor(40, 40, 50, 80))
        pen2.setWidth(1)
        painter.setPen(pen2)
        painter.drawPath(inner_path)
        
    @QtCore.Slot()
    def handle_search(self):
        search_text = self.search_bar.text().strip()
        if search_text:
            print(f"Searching for: {search_text}")
            # Add your search functionality here
            
    @QtCore.Slot(str)
    def handle_text_changed(self, text):
        # Call the registered callback if it exists
        if self.text_changed_callback:
            self.text_changed_callback(text)
            
        # Hide suggestions if text is empty
        if len(text) == 0:
            self.hide_suggestions()
    
    def set_text_changed_callback(self, callback):
        """Set the callback function that gets called when text changes"""
        self.text_changed_callback = callback
        
    def set_suggestions(self, suggestions):
        """Set suggestions to display"""
        if isinstance(suggestions, str):
            suggestions = [suggestions]
            
        self.current_suggestions = suggestions
        self.update_suggestions_display()
        
    def update_suggestions_display(self):
        """Update the suggestions display based on current suggestions"""
        if not self.current_suggestions:
            self.hide_suggestions()
            return
            
        self.suggestions_display.set_suggestions(self.current_suggestions)
        self.show_suggestions()
        
    def show_suggestions(self):
        """Show the suggestions display and resize window"""
        if not self.suggestions_display.isVisible():
            self.suggestions_display.setVisible(True)
            
            # Calculate new height
            suggestions_height = self.suggestions_display.get_suggested_height()
            new_height = self.base_height + suggestions_height
            self.setFixedSize(600, new_height)
            
    def hide_suggestions(self):
        """Hide the suggestions display and resize window back"""
        if self.suggestions_display.isVisible():
            self.suggestions_display.setVisible(False)
            self.setFixedSize(600, self.base_height)
            
    @QtCore.Slot(str)
    def on_suggestion_selected(self, suggestion):
        """Handle when a suggestion is clicked"""
        self.search_bar.setText(suggestion)
        self.hide_suggestions()
        self.handle_search()
            
    def keyPressEvent(self, event):
        # Close on Escape key
        if event.key() == QtCore.Qt.Key_Escape:
            if self.suggestions_display.isVisible():
                self.hide_suggestions()
            else:
                self.close()
        # Navigate suggestions with arrow keys
        elif event.key() == QtCore.Qt.Key_Down and self.suggestions_display.isVisible():
            self.suggestions_display.suggestions_list.setFocus()
            if self.suggestions_display.suggestions_list.count() > 0:
                self.suggestions_display.suggestions_list.setCurrentRow(0)
        elif event.key() == QtCore.Qt.Key_Up and self.suggestions_display.isVisible():
            self.suggestions_display.suggestions_list.setFocus()
            if self.suggestions_display.suggestions_list.count() > 0:
                self.suggestions_display.suggestions_list.setCurrentRow(self.suggestions_display.suggestions_list.count() - 1)
        super().keyPressEvent(event)
        
    def mousePressEvent(self, event):
        # Enable dragging when clicking anywhere on the window
        if event.button() == QtCore.Qt.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        # Move window when dragging
        if event.buttons() == QtCore.Qt.LeftButton and self.drag_position is not None:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
    
    def mouseReleaseEvent(self, event):
        # Stop dragging
        if event.button() == QtCore.Qt.LeftButton:
            self.drag_position = None
            event.accept()

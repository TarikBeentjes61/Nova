import sys
from PySide6 import QtCore, QtWidgets, QtGui
from nova.ui import MainWindow

def text_changed_callback(text):
    suggestions = []
    for letter in "abcdefghijklmnopqrstuvwxyz":
        suggestions.append(f"{text}{letter}")
    window.set_suggestions(suggestions)

def main():
    global window
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.set_text_changed_callback(text_changed_callback)
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()

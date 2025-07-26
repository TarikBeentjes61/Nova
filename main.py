import sys
import json
from PySide6 import QtWidgets
from nova.ui import MainWindow

# Load commands from JSON
with open("commands.json", "r") as f:
    data = json.load(f)
    COMMANDS = data.get("commands", [])

def text_changed_callback(text):
    text = text.strip()
    tokens = text.split()

    suggestions = []

    if not text:
        # Show all commands when input is empty
        suggestions = [cmd["name"] for cmd in COMMANDS]
    else:
        first_word = tokens[0].lower()
        matching_command = next((cmd for cmd in COMMANDS if cmd["name"].lower() == first_word), None)

        if matching_command:
            # Track which parameters have been used
            used_params = set()
            last_token = tokens[-1]

            for t in tokens[1:]:
                # Remove "-" or "--"
                if t.startswith("-"):
                    used_params.add(t.lstrip("-"))

            # If last token is a flag that requires input
            for param in matching_command["parameters"]:
                if last_token in (f"-{param['short']}", f"-{param['name']}") and param["input"]:
                    # Suggest placeholder for input value
                    suggestions = [f"<{param['name']} value>"]
                    break
            else:
                # Suggest remaining flags
                for param in matching_command["parameters"]:
                    if param["short"] not in used_params and param["name"] not in used_params:
                        suggestions.append(f"-{param['short']}")
        else:
            # Suggest commands that start with typed text
            for cmd in COMMANDS:
                if cmd["name"].startswith(first_word):
                    suggestions.append(cmd["name"])

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

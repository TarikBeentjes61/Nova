import sys
import json
from PySide6 import QtWidgets
from nova.ui import MainWindow

"""
Command Categories:
File → File operations (copy, move, delete, etc.)
Disk → Disk utilities (format, chkdsk, diskpart)
System → System control (shutdown, tasklist, taskkill)
Network → Network utilities (ping)
Process → Process management (tasklist, taskkill)
Directory → Directory navigation and management (cd, dir, tree, mkdir, rd)
Interpreter → Commands related to the CMD environment (cmd, echo, exit, help)
Boot → Boot configuration (bcdedit)
Permissions → File permissions and attributes (attrib, cacls)

Command Types:
cmd
powershell
bash
custom
python
git
system
...
"""

with open("custom_commands.json", "r") as f:
    data_custom = json.load(f)
    CUSTOM_COMMANDS = data_custom.get("custom", [])

with open("cmd_commands.json", "r") as f:
    data_cmd = json.load(f)
    CMD_COMMANDS = data_cmd.get("windows", [])

ALL_COMMANDS = CMD_COMMANDS + CUSTOM_COMMANDS

def text_changed_callback(text):
    text = text.strip()
    tokens = text.split()

    suggestions = []

    if not text:
        suggestions = [cmd["name"] for cmd in ALL_COMMANDS]
    else:
        first_word = tokens[0].lower()
        matching_command = next((cmd for cmd in ALL_COMMANDS if cmd["name"].lower() == first_word), None)

        if matching_command:
            used_params = set()
            for t in tokens[1:]:
                if t.startswith("-"):
                    used_params.add(t.lstrip("-"))

            # Suggest remaining parameters/flags for this command
            for param in matching_command.get("parameters", []):
                if param["short"] not in used_params and param["name"] not in used_params:
                    suggestions.append(f"-{param['short']}" if param.get("short") else f"--{param['name']}")
        else:
            # Suggest commands that start with typed text
            for cmd in ALL_COMMANDS:
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
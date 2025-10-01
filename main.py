import sys
import json
from PySide6.QtWidgets import QApplication
from nova.ui import MainWindow
from nova.core.discover import discover_programs

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

def main():
    discovered = discover_programs(limit=250)

    json_str = json.dumps(discovered, indent=4)
    with open("programs.json", "w") as f:
        f.write(json_str)

    app = QApplication(sys.argv)
    window = MainWindow()
    app.installEventFilter(window)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
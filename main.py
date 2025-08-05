import sys
from PySide6.QtWidgets import QApplication
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

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
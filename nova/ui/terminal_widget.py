from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit
from PySide6.QtCore import QProcess
import psutil

class TerminalWidget(QWidget):
    def __init__(self, name: str):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.name = name

        self.terminal_display = QTextEdit()
        self.terminal_display.setReadOnly(True)
        self.terminal_display.setStyleSheet("""
            QTextEdit {
                background-color: #1E1E1E;
                color: #FFFFFF;
                font-family: Consolas, monospace;
                font-size: 10pt;
            }
        """)
        layout.addWidget(self.terminal_display)

        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.on_stdout)
        self.process.readyReadStandardError.connect(self.on_stderr)
        
        self.process.start("cmd.exe", ["/q"])
        self.process_id = self.process.processId()
    
    # check if a process is running or not
    def get_state(self):
        try:
            if self.process_id:
                proc = psutil.Process(self.process_id)
                if proc.children():
                    return True
                else:
                    return False
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return False

    def on_stdout(self):
        data = self.process.readAllStandardOutput()
        text = data.data().decode('utf-8', errors='ignore')
        self.terminal_display.append(text)
        
    def on_stderr(self):
        data = self.process.readAllStandardError()
        text = data.data().decode('utf-8', errors='ignore')
        self.terminal_display.append(f'<span style="color: red;">{text}</span>')

    def send_input(self, input: str):
        if not self.get_state():
            if not input.endswith('\n'):
                input += '\n'
            self.process.write(input.encode())
            self.terminal_display.append(f'<span style="color: #66FF66">{input}</span>')
        else:
            self.terminal_display.append('<span style="color: red">[Cannot send input - process is busy]</span>')

    def close(self):
        self.process.terminate()
        super().close()
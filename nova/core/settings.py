from PySide6.QtCore import QObject, Signal

import json
class AppSettings(QObject):
    _instance = None
    settings_changed = Signal(list)

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.load_settings()
        return cls._instance

    def get(self, key, default=None):
        return self.data.get(key, default)
    
    def set(self, key, value):
        if key in self.data:
            self.data[key] = value
            self.settings_changed.emit(self.data)
            self.save_settings()

    def load_settings(self):
        self.data = {}
        with open("nova/core/settings.json", "r") as f:
            self.data = json.load(f)

    def save_settings(self):
        with open("nova/core/settings.json", "w") as f:
            json.dump(self.data, f, indent=4)
        self.settings_changed.emit(self.data)

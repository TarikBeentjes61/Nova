from nova.model.suggestion import Suggestion

class Program(Suggestion):
    def __init__(self, name: str, description: str, category: str, command_type: str, exe: str, icon: str):
        super().__init__(name, description, category, command_type)
        self.exe = exe
        self.icon = icon
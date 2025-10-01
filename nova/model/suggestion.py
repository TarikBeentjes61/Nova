from enum import Enum

class CommandType(Enum):
    EXECUTABLE = "executable"
    CUSTOM = "custom"
    CMD = "cmd"

class Suggestion():
    def __init__(self, name: str, description: str, category: str, command_type: str):
        self.name = name
        self.description = description
        self.category = category
        self.command_type = CommandType(command_type) if command_type in CommandType._value2member_map_ else CommandType.CUSTOM







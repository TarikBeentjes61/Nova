from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

class CommandType(Enum):
    EXECUTABLE = "executable"
    CUSTOM = "custom"
    CMD = "cmd"

@dataclass
class Suggestion:
    name: str
    description: Optional[str]
    category: str
    command_type: CommandType

@dataclass
class Program(Suggestion):
    exe: str
    icon: str

class Parameter():
    def __init__(self, name, required=False, input_=False, description=""):
        self.name = name
        self.required = required
        self.input = input_
        self.description = description

@dataclass
class Custom(Suggestion):
    command: str
    parameters: list[Parameter] = field(default_factory=list)

@dataclass
class Cmd(Suggestion):
    example: str
    parameters: list[Parameter] = field(default_factory=list)

def suggestion_from_dict(data: dict, source_file: str = None):
    try:
        ctype = data.get("command_type", "custom")

        if ctype == "cmd":
            return Cmd(
                name=data["name"],
                description=data.get("description", ""),
                category=data.get("category", "Unknown"),
                command_type=CommandType.CMD,
                example=data["example"],
                parameters = [
                    Parameter(
                        name=p["name"],
                        input_=p.get("input", False),
                        required=p.get("required", False),
                        description=p.get("description", "")
                    )
                    for p in data.get("parameters", [])
                ]
            )
        elif ctype == "executable":
            return Program(
                name=data["name"],
                description=data.get("description", ""),
                category=data.get("category", "Unknown"),
                command_type=CommandType.EXECUTABLE,
                exe=data["exe"],
                icon=data["icon"]
            )
        else:
            return Custom(
                name=data["name"],
                description=data.get("description", ""),
                category=data.get("category", "Unknown"),
                command_type=CommandType.CUSTOM,
                command=data["command"],
                parameters = [
                    Parameter(
                        name=p["name"],
                        input_=p.get("input", False),
                        required=p.get("required", False),
                        description=p.get("description", "")
                    )
                    for p in data.get("parameters", [])
                ]
            )
    except KeyError as e:
        raise KeyError(f"Missing key {e} in file {source_file or '<unknown>'}")

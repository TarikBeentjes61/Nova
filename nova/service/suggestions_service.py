import json
from nova.model.command import Command, Parameter
from nova.model.program import Program
from nova.model.suggestion import Suggestion

class SuggestionsService:
    def __init__(self):
        self.commands = self.get_commands()
        self.programs = self.get_programs()
        self.all_suggestions = self.commands + self.programs

    def get_commands(self):
        commands = []   
        for filename in ["custom_commands.json", "cmd_commands.json"]:
            with open(filename, "r") as f:
                data = json.load(f)
                for key in data:
                    for entry in data[key]:
                        commands.append(Command(
                            name=entry.get("name", ""),
                            description=entry.get("description", ""),
                            category=entry.get("category", ""),
                            command_type=entry.get("command_type", ""),
                            example=entry.get("example", ""),
                            parameters=[
                                Parameter(
                                    name=param.get("name", ""),
                                    short=param.get("short", ""),
                                    required=param.get("required", False),
                                    input_=param.get("input", False),
                                    description=param.get("description", "")
                                ) for param in entry.get("parameters", [])
                            ]
                        ))
        return commands

    def get_programs(self):
        with open("programs.json", "r") as f:
            data = json.load(f)
            programs = []
            for entry in data:
                programs.append(Program(
                    name=entry.get("name", ""),
                    description=entry.get("description", "") or f"{entry.get('name', '')} application",
                    category=entry.get("category", "Application"),
                    command_type=entry.get("command_type", "executable"),
                    exe=entry.get("exe", ""),
                    icon=entry.get("icon", "")
                ))
            return programs

    def get_suggestions(self, input_text: str):
        input_text = input_text.strip()
        tokens = input_text.split()
        suggestions = []

        if not input_text or input_text == "":
            return self.all_suggestions, None

        first_word = tokens[0].lower()

        # search for exact match first
        matching_suggestion = next((suggestion for suggestion in self.all_suggestions if suggestion.name.lower() == first_word), None)
        if matching_suggestion:
            print(f"Exact match found: {matching_suggestion}")
            used_parameters = set(t.lstrip("-+/") for t in tokens[1:])
            if isinstance(matching_suggestion, Command):
                for param in matching_suggestion.parameters:
                    if param.short not in used_parameters and param.name not in used_parameters:
                        suggestions.append(param)
            return suggestions, matching_suggestion

        # suggest anything that starts with the input
        for item in self.all_suggestions:
            if item.name.lower().startswith(first_word):
                suggestions.append(item)

        return suggestions, matching_suggestion

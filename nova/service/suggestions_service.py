import json
from nova.model.command import Command, Parameter

class SuggestionsService:
    def __init__(self):
        self.commands = self.get_commands()

    def get_commands(self):
        commands = []

        for filename in ["custom_commands.json", "cmd_commands.json"]:
            with open(filename, "r") as f:
                data = json.load(f)
                for key in data:
                    for cmd_dict in data[key]:
                        commands.append(Command.from_dict(cmd_dict))
        return commands
    
    def get_suggestions(self, input_text):
        input_text = input_text.strip()
        tokens = input_text.split()
        suggestions = []

        if not input_text:
            return self.commands

        first_word = tokens[0].lower()
        matching_command = next((cmd for cmd in self.commands if cmd.name.lower() == first_word), None)

        if matching_command:
            used_parameters = set()
            for t in tokens[1:]:
                cleaned = t.lstrip("-+/") 
                used_parameters.add(cleaned)

            for param in matching_command.parameters:
                if param.short not in used_parameters and param.name not in used_parameters:
                    suggestions.append(param)

            return suggestions

        else:
            for command in self.commands:
                if command.name.lower().startswith(first_word):
                    suggestions.append(command)

        return suggestions


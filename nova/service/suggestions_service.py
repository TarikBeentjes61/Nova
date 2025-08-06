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
            last_token = tokens[-1].lower()

            #find used parameters
            used_parameters = set()
            for t in tokens[1:]:
                if t.startswith("-"):
                    used_parameters.add(t.lstrip("-"))

            #check if last token needs input
            for param in matching_command.parameters:
                if last_token == f"-{param.short}" and param.input:
                    return []

            #add unused parameters
            for param in matching_command.parameters:
                if param.short not in used_parameters and param.name not in used_parameters:
                    suggestions.append(param)

            return suggestions
        else:
            #suggest commands that match the first word
            for command in self.commands:
                if command.name.lower().startswith(first_word):
                    suggestions.append(command)

        return suggestions

import json

class SuggestionsService:
    def __init__(self):
        self.commands = self.get_commands()

    def get_commands(self):
        with open("custom_commands.json", "r") as f:
            data_custom = json.load(f)
            custom_commands = data_custom.get("custom", [])

        with open("cmd_commands.json", "r") as f:
            data_cmd = json.load(f)
            cmd_commands = data_cmd.get("windows", [])

        return cmd_commands + custom_commands
    
    def get_suggestions(self, input_text):
        input_text = input_text.strip()
        tokens = input_text.split()

        suggestions = []

        if not input_text:
            suggestions = [cmd["name"] for cmd in self.commands]
        else:
            first_word = tokens[0].lower()
            matching_command = next((cmd for cmd in self.commands if cmd["name"].lower() == first_word), None)

            if matching_command:
                used_params = set()
                for t in tokens[1:]:
                    if t.startswith("-"):
                        used_params.add(t.lstrip("-"))

                # Suggest remaining parameters/flags for this command
                for param in matching_command.get("parameters", []):
                    if param["short"] not in used_params and param["name"] not in used_params:
                        suggestions.append(f"-{param['short']}" if param.get("short") else f"--{param['name']}")
            else:
                # Suggest commands that start with typed text
                for cmd in self.commands:
                    if cmd["name"].startswith(first_word):
                        suggestions.append(cmd["name"])

        return suggestions
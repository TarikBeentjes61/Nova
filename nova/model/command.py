from nova.model.suggestion import Suggestion

class Parameter:
    def __init__(self, name, short, required, input_, description):
        self.name = name
        self.short = short
        self.required = required
        self.input = input_
        self.description = description
    
class Command(Suggestion):
    def __init__(self, name: str, description: str, category: str, command_type: str, example: str, parameters: list):
        super().__init__(name, description, category, command_type)
        self.example = example
        self.parameters = parameters
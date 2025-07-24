class Command:
    def __init__(self, name, description, example, help, parameters=None):
        self.name = name
        self.description = description
        self.example = example
        self.help = help
        self.parameters = parameters if parameters is not None else []

    def __repr__(self):
        return f"Command(name={self.name}, description={self.description}, parameters={self.parameters})"

class Parameter:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return f"{self.name}"
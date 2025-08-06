class Command:
    def __init__(self, name, description, example, parameters, category, command_type):
        self.name = name
        self.description = description
        self.example = example
        self.parameters = parameters
        self.category = category
        self.command_type = command_type

    @classmethod
    def from_dict(cls, d):
        params = [Parameter(
            p.get("name", ""),
            p.get("short", ""),
            p.get("required", False),
            p.get("input", False),
            p.get("description", ""),
        ) for p in d.get("parameters", [])]
        return cls(
            d.get("name", ""),
            d.get("description", ""),
            d.get("example", ""),
            params,
            d.get("category", ""),
            d.get("command_type", ""),
        )

    def __repr__(self):
        return f"Command(name={self.name})"
    
class Parameter:
    def __init__(self, name, short, required, input_, description):
        self.name = name
        self.short = short
        self.required = required
        self.input = input_
        self.description = description

    def __repr__(self):
        return f"Parameter(name={self.name}, short={self.short})"

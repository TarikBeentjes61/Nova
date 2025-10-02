import json
import os
from nova.model.suggestion import CommandType, Custom, Suggestion, Cmd, Parameter, Program, suggestion_from_dict

class SuggestionsService:
    def __init__(self):
        folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "suggestions")
        self.all_suggestions = self.load_suggestions_from_folder(folder)

    def load_suggestions_from_folder(self, folder: str):
        suggestions = []
        for root, _, files in os.walk(folder):
            for filename in files:
                if filename.endswith(".json"):
                    filepath = os.path.join(root, filename)
                    with open(filepath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if isinstance(data, dict):
                            suggestions.append(suggestion_from_dict(data, filepath))
                        elif isinstance(data, list):
                            for item in data:
                                suggestions.append(suggestion_from_dict(item, filepath))
        return suggestions


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
            used_parameters = set(t for t in tokens[1:])
            if isinstance(matching_suggestion, Cmd) or isinstance(matching_suggestion, Custom):
                for param in matching_suggestion.parameters:
                    if param.name not in used_parameters:
                        suggestions.append(param)
            return suggestions, matching_suggestion
            
        # suggest anything that starts with the input
        for item in self.all_suggestions:
            if item.name.lower().startswith(first_word):
                suggestions.append(item)

        return suggestions, matching_suggestion

import os
from nova.model.command import Command, Parameter
from nova.model.suggestion import Suggestion
from nova.model.program import Program

class CommandService:
    def __init__(self):
        self.history = [] # from file
        pass

    def execute(self, input: str, suggestion: Suggestion):
          if isinstance(suggestion, Program):
               print(f"Executing program: {suggestion.exe}")
               os.system(suggestion.exe)
          return "Command executed"
    
    def execute_cmd(self, input):
         pass

    def execute_custom(self, input):
         pass
    
    def execute_exe(self, input):
         pass
    
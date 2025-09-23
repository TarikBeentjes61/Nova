from nova.model.command import Command, Parameter
from nova.model.suggestion import Suggestion
from nova.model.program import Program

class CommandService:
     def __init__(self, terminalManager):
          self.history = [] # from file
          self.terminalManager = terminalManager

     def execute(self, input_text: str, suggestion: Suggestion):
          if isinstance(suggestion, Command):
               terminal = self.terminalManager.active_terminal
               if terminal and terminal.is_running() == False:
                    terminal.send_input(input_text + "\n")
                    self.history.append(input_text)
                    return f"Executed command: {input_text}"
               else:
                    return "No active terminal to execute the command."
              


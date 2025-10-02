from nova.model.suggestion import Suggestion, Cmd, Custom, Program
class CommandService:
     def __init__(self, terminalManager_widget):
          self.history = [] # from file
          self.terminalManager_widget = terminalManager_widget

     # check for available terminal or create a new one and execute the command
     def execute(self, input_text: str, suggestion: Suggestion):
          if isinstance(suggestion, Cmd):
               terminal = self.terminalManager_widget.get_available_terminal()
               if terminal:
                    self.terminalManager_widget.open_terminal(terminal)
                    terminal.send_input(input_text)
                    self.history.append(input_text)
               else:
                    name = str(self.terminalManager_widget.get_terminal_count() + 1)
                    self.terminalManager_widget.new_terminal(name)
                    terminal = self.terminalManager_widget.get_terminal(name)
                    terminal.send_input(input_text)
                    self.history.append(input_text)
          elif isinstance(suggestion, Program):
               pass
          elif isinstance(suggestion, Custom):
               pass
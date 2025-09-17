import os

class CommandService:
    def __init__(self):
        pass

    def execute(self, input):
            print(f"Executing command: {input}")

            #check command type, 

            os.system(input)

            return "Command executed"
    
    def execute_cmd(self, input):
         pass

    def execute_custom(self, input):
         pass
    
    def execute_exe(self, input):
         pass
    
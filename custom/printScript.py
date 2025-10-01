import sys
from enum import Enum

class PrintMode(Enum):
    NORMAL = 1
    UPPER = 2
    LOWER = 3

def how_to_use():
    print("""Usage: print [options] <text>""")

if __name__ == "__main__":
    args = sys.argv[1:]
    mode = PrintMode.NORMAL
    text = ""
    for arg in args:
        if arg in ("--upper", "-u"):
            if mode == PrintMode.LOWER:
                print("Error: Cannot use both --upper and --lower options together.")
                sys.exit(1)
            mode = PrintMode.UPPER
        elif arg in ("--lower", "-l"):
            if mode == PrintMode.UPPER:
                print("Error: Cannot use both --upper and --lower options together.")
                sys.exit(1)
            mode = PrintMode.LOWER
        else:
            text += arg + " "
    print(text.upper().strip() if mode == PrintMode.UPPER else text.lower().strip() if mode == PrintMode.LOWER else text.strip())


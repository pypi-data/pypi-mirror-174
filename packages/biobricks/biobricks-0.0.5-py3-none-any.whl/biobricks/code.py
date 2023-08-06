import os
import sys
from tkinter import filedialog

# Pointer to the module object instance itself
this = sys.modules[__name__]

# Location of biobricks library
this.lib = None

# Current version
def version():
    return("BioBricks Version 0.0.3")

def load(brick):
    if (this.lib is None):
        bblib = os.getenv("bblib")
        if bblib:
            this.lib = bblib
        else:
            bblib = filedialog.askdirectory()
            this.lib = bblib
        os.system(f"cd {this.lib}; git init")
        os.system(f"cd {this.lib}; mkdir cache")
        print(f"Initialized BioBricks library to {this.lib}.")
    else:
        print(f"Loading brick {brick} from {this.lib}.")

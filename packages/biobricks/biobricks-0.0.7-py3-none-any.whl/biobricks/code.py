import os
import sys
import pkg_resources
from tkinter import filedialog

# Pointer to the module object instance itself
this = sys.modules[__name__]

# Location of biobricks library
this.lib = None

# Current version
def version():
    version = pkg_resources.get_distribution("biobricks").version
    print(f"BioBricks Version {version}")

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

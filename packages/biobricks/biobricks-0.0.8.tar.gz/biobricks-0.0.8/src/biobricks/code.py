import os
# import sys
import pkg_resources
from tkinter import filedialog

# Pointer to the module object instance itself
# this = sys.modules[__name__]

# Location of biobricks library
lib = None

# Current version
def version():
    version = pkg_resources.get_distribution("biobricks").version
    print(f"BioBricks Version {version}")

def load(brick):
    global lib
    if (lib is None):
        bblib = os.getenv("bblib")
        if bblib:
            lib = bblib
        else:
            bblib = filedialog.askdirectory()
            # TODO: Check if dialog was cancel
            lib = bblib
        os.system(f"cd {lib}; git init")
        os.system(f"cd {lib}; mkdir cache")
        print(f"Initialized BioBricks library to {lib}.")
    else:
        print(f"Loading brick {brick} from {lib}.")

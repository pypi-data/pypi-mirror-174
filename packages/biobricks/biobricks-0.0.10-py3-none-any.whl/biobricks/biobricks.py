import os
import pkg_resources
from tkinter import filedialog

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
            lib = "~/bblib"
        os.system(f"cd {lib}; git init")
        os.system(f"cd {lib}; mkdir cache")
        print(f"Initialized BioBricks library to {lib}.")
    else:
        print(f"Loading brick {brick} from {lib}.")

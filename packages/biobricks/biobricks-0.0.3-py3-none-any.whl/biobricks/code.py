import os
from tkinter import filedialog

def version():
    return("BioBricks Version 0.0.3")

def initialize():
    bblib = os.getenv("bblib")
    if bblib:
        print(f"{bblib=}")
    else:
        bblib = filedialog.askdirectory()
    os.system(f"cd {bblib}; git init")
    os.system(f"cd {bblib}; mkdir cache")
    print(f"Initialized biobricks to {bblib}")


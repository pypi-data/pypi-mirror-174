import os
from os.path import exists
import pkg_resources
import json
from typing import Any, Dict

# Location of biobricks
BASE_DIR = os.path.expanduser('~')+'/biobricks'
CONFIG_FILE = BASE_DIR+'/config.json'
library = None

# Current version
def version():
    version = pkg_resources.get_distribution("biobricks").version
    print(f"BioBricks Version {version}")

def load(brick):
    initialize()
    print(f"Loading brick {brick} from {library}.")

def read_config() -> Dict[str, Any]:
    with open(CONFIG_FILE) as f:
        return json.load(f)

def write_config(config: Dict[str, Any]) -> None:
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

def initialize() -> None:
    global library
    os.makedirs(BASE_DIR, exist_ok=True)
    if exists(CONFIG_FILE):
        config = read_config()
        library = config["library"]
        print(f"BioBricks library already intialized to {library}.")
    else:
        bblib = os.getenv("bblib")
        if bblib:
            library = bblib
        else:
            library = BASE_DIR+'/library'
        config = { 'library': library, }
        write_config(config)
        os.makedirs(library, exist_ok=True)
        os.makedirs(library+"/cache", exist_ok=True)
        if not exists(library+"/.git"):
            os.system(f"cd {library}; git init")
        print(f"Initialized BioBricks library to {library}.")

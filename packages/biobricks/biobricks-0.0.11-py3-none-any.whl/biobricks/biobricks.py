import os
import pkg_resources
import json
from typing import Any, Dict

# Location of biobricks library
CONFIG_FILE = '~/biobricks/config.json'

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
    try:
        config = read_config()
    except FileNotFoundError:
        bblib = os.getenv("bblib")
        if bblib:
            library = bblib
        else:
            library = '~/biobricks/library'
        config = {
            'library': library,
        }
        write_config(config)
        os.system(f"cd {library}; git init")
        os.system(f"cd {library}; mkdir -p cache")
        print(f"Initialized BioBricks library to {library}.")
    globals().update(config)
    
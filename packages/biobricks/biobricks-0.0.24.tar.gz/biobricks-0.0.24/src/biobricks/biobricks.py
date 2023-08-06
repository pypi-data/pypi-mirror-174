import os
from os.path import exists
import pkg_resources
import json
from typing import Any, Dict

# Location of biobricks
BASE_DIR = os.path.expanduser('~')+'/biobricks'
CONFIG_FILE = BASE_DIR+'/config.json'
config = None
library = None
bricks = []

def version():
    version = pkg_resources.get_distribution("biobricks").version
    print(f"BioBricks Version {version}")

def initialize() -> None:
    global config, library, bricks
    os.makedirs(BASE_DIR, exist_ok=True)
    if exists(CONFIG_FILE):
        with open(CONFIG_FILE) as file:
            config = json.load(file)
        library = config["library"]
        bricks = config["bricks"]
        print(f"BioBricks library already intialized to {library}.")
    else:
        bblib = os.getenv("bblib")
        if bblib:
            library = bblib
        else:
            library = BASE_DIR+'/library'
        config = { 'library': library, 'bricks': [], }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)
        os.makedirs(library, exist_ok=True)
        os.makedirs(library+"/cache", exist_ok=True)
        if not exists(library+"/.git"):
            os.system(f"cd {library}; git init")
        print(f"Initialized BioBricks library to {library}.")

def load(brick):
    global config, bricks
    initialize()
    if not brick in bricks:
        print(f"Pulling brick {brick} from GitHub.")
        repo = "biobricks-ai/"+brick
        url = "https://github.com/"+repo
        repodir = library+"/"+repo
        os.system(f"cd {library}; git submodule add {url} {repo}")
        os.system(f"cd {repodir}; dvc cache dir ../../cache")
        os.system(f"cd {repodir}; dvc config cache.shared group")
        os.system(f"cd {repodir}; dvc config cache.type symlink")
        for i in range(3):
            print(f"Attemp {i} to pull")
            code = os.system(f"cd {repodir}; dvc pull brick")
            print(f"Pulling output code: {code}")
            if code==0:
                break
        os.system(f"cd {library}; git commit -m \"added {repo}\"")
        bricks += [brick]
        config['bricks'] = bricks
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)
    print(f"Loading brick {brick} from local library.")


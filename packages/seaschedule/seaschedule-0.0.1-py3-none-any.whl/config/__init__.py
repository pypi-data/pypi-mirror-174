import os

from datetime import datetime
from importlib import resources
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


# Read environment
try:
    ENV = os.environ["PYTHON_ENV"]
    CFG_FILE = f"config_{ENV}.toml"
except KeyError as e:
    ENV = ""
    CFG_FILE = f"config.toml"

# Read configuration file
CFG = tomllib.loads(resources.read_text("config", CFG_FILE, encoding="utf-8"))

# Additional configurations
RUN_TIME = datetime.now()
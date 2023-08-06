import os
from pathlib import Path

PSENV_HOME = Path("~/.psenv").expanduser()
PSENV_YML = PSENV_HOME / "psenv.yml"
PSENV_PUSH_EXCLUDE = os.getenv("PSENV_PUSH_EXCLUDE", "AWS_, ").split(",")

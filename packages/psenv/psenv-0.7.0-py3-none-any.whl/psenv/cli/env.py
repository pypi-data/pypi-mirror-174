from argparse import Namespace
from psenv.core.helpers import parse_config, save_config


def new_entrypoint(cmd: Namespace) -> None:
    config = parse_config()

    new_entry = {cmd.env: {"path": cmd.path, "env": cmd.file}}

    config["environments"].update(**new_entry)
    save_config(config)


def destroy_entrypoint(cmd: Namespace) -> None:
    print("hulk smash!!")

from argparse import Namespace
from pathlib import Path
from dotenv import dotenv_values
from psenv.core.helpers import parse_config, filter_on_exclusion
from psenv.core.parameter_store import ParameterStore


def push_entrypoint(cmd: Namespace) -> None:

    config = parse_config()["environments"][cmd.env]
    env_file = Path(config["env"]).expanduser()
    path = config["path"]

    parameter_store = ParameterStore(path=path)

    params = dotenv_values(env_file)

    if "exclude_prefixes" in config.keys():
        params = filter_on_exclusion(params, config["exclude_prefixes"])
    parameter_store.push_to_parameter_store(params=params, overwrite=cmd.overwrite)

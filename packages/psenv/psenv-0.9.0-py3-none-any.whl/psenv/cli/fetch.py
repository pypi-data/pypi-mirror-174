from argparse import Namespace
from pathlib import Path
from psenv.environment.variables import PSENV_YML
from psenv.core.parameter_store import ParameterStore
from psenv.core.env_file import EnvFile
from psenv.core.helpers import parse_config


def fetch_entrypoint(cmd: Namespace) -> None:

    try:
        config = parse_config()["environments"][cmd.env]
    except KeyError:
        print(f"environment {cmd.env} not found in .psenv.yml config file.")
        exit()
    except Exception:
        print("unknown exception encountered... no idea why.")

    # make things with parameters
    parameter_store = ParameterStore(path=config["path"])
    params = parameter_store.get_parameters_by_path()
    params = parameter_store.parse_params_to_key_value_pairs(params)

    env_path = Path(config["env"])
    env_file = EnvFile(path=env_path)
    env_file.write_params_to_env(params=params, method=cmd.method)

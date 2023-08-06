import os
import yaml
from typing import Dict, List, Any
from psenv.environment.variables import PSENV_YML


def parse_config() -> Dict[str, Any]:
    with PSENV_YML.open() as yml_config:
        return yaml.safe_load(yml_config)


def save_config(config: Dict[str, Dict[str, str]]) -> None:
    with PSENV_YML.open(mode="w+") as yml_config:
        yaml.dump(data=config, stream=yml_config)


def filter_on_exclusion(environment: Dict[str, str], exclusion_prefixes: List[str]) -> Dict[str, str]:
    return {key: value for key, value in environment.items() for pre in exclusion_prefixes if not key.startswith(pre)}


def get_environment_variables(prefix: str) -> Dict[str, str]:
    retrieved = {}
    for key, value in os.environ.items():
        if key.startswith(prefix):
            retrieved[key] = value
    return retrieved

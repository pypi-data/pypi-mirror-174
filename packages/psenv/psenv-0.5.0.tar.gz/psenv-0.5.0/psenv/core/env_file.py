from pathlib import Path
from typing import Dict, List
from dotenv import dotenv_values


class EnvFile:
    def __init__(self, path: Path) -> None:
        self.path = path

        self._methods = {"overwrite": self._overwrite_env, "update": self._update_env}

    def write_params_to_env(self, params: Dict[str, str], method: str = "overwrite") -> None:

        if method not in self._methods.keys():
            raise ValueError(f"available methods are {self._methods.keys()} got {method} instead")

        method = self._methods.get(method)
        method(params=params)

    @staticmethod
    def _get_sorted_keys(params: Dict[str, str]) -> List[str]:
        return sorted(params.keys())

    def _overwrite_env(self, params: Dict[str, str]) -> None:
        keys = self._get_sorted_keys(params)

        with self.path.open("w+") as env:
            ref_prefix = ""
            for i, key in enumerate(keys):

                current_prefix = key.split("_")[0]
                if current_prefix != ref_prefix and i > 0:
                    ref_prefix = current_prefix
                    env.write("\n")
                    env.write(f"# ----------------------------{current_prefix}------------------------------------ #\n")

                value = params[key]
                line = f"{key}={value}"
                env.write(f"{line}\n")

    def _update_env(self, params: Dict[str, str]) -> None:
        current_values = dotenv_values(self.path)
        current_values.update(**params)
        self._overwrite_env(current_values)

from argparse import Namespace
from psenv.environment.variables import PSENV_YML, PSENV_HOME


def init_entrypoint(cmd: Namespace) -> None:

    PSENV_HOME.mkdir(exist_ok=True)

    if PSENV_YML.exists():
        print("existing .psenv.yml found in ~/.psenv.yml")
        # exit()

    content = """
environments:
    default:
        path: /some/path/to/params
        env: /path/to/envfile
    """

    PSENV_YML.touch(exist_ok=True)
    PSENV_YML.write_text(content)

from argparse import ArgumentParser, Action, Namespace
from typing import Any
from psenv.core.helpers import parse_config


def validate_input_string(input_string: str, message: str) -> None:
    forbidden = "!" "#$%&'()*+,./:;<=>?@[\\]^`{|}~"
    for char in input_string:
        if char in forbidden:
            print(message)
            exit()


def validate_path_name(path_string: str) -> None:
    forbidden = "!" "#$%&'()*+,.:;<=>?@[\\]^`{|}~"
    for char in path_string:
        if char in forbidden:
            print(f"the character {char} is forbidden in path names.")
            exit()


def validate_file_name(path_string: str) -> None:
    forbidden = "!" "#$%&'()*+,:;<=>?@[\\]^`{|}~"
    for char in path_string:
        if char in forbidden:
            print(f"the character {char} is forbidden in path names.")
            exit()


def validate_environment_exists(environment: str) -> None:
    environments = parse_config()["environments"].keys()
    if environment in environments:
        print(f"The environment {environment} already exists. Please choose another name or remove existing entry.")
        exit()


def validate_environment_does_not_exist(environment: str) -> None:
    environments = parse_config()["environments"].keys()
    if environment not in environments:
        print(f"The environment {environment} does not exist. run psenv show to list configured environments.")
        exit()


class ValidateEnvironmentName(Action):
    def __call__(self, parser: ArgumentParser, namespace: Namespace, values: Any, option_string: str = None):
        validate_input_string(values, f"The {values} is not allowed in environment names.")

        if namespace.func.__name__ == "new_entrypoint":
            validate_environment_exists(values)

        if namespace.func.__name__ in ["destroy_entrypoint", "fetch_entrypoint", "push_entrypoint"]:
            validate_environment_does_not_exist(values)
        setattr(namespace, self.dest, values)


class ValidatePathName(Action):
    def __call__(self, parser: ArgumentParser, namespace: Namespace, values: Any, option_string: str = None):
        if namespace.path:
            validate_path_name(values)
        setattr(namespace, self.dest, values)


class ValidateFileName(Action):
    def __call__(self, parser: ArgumentParser, namespace: Namespace, values: Any, option_string: str = None):
        if namespace.path:
            validate_file_name(values)
        setattr(namespace, self.dest, values)

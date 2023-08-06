import boto3
from typing import Dict


class ParameterStore:
    def __init__(self, path: str) -> None:
        self.path = path
        self.ssm_client = boto3.client("ssm")

    def get_parameters_by_path(self) -> Dict[str, str]:

        params = {}
        next_token = ""

        while True:

            if next_token:
                response = self.ssm_client.get_parameters_by_path(
                    Path=self.path, Recursive=True, WithDecryption=True, NextToken=next_token
                )
            else:
                response = self.ssm_client.get_parameters_by_path(Path=self.path, Recursive=True, WithDecryption=True)

            params.update(**{p["Name"].upper(): p["Value"] for p in response["Parameters"] if "\n" not in p["Value"]})

            try:
                next_token = response["NextToken"]
            except KeyError:
                break

        return params

    @staticmethod
    def parse_params_to_key_value_pairs(params: Dict[str, str]) -> Dict[str, str]:
        return {key.split("/")[-1]: value for key, value in params.items()}

    def push_to_parameter_store(self, params: Dict[str, str], overwrite: bool = False) -> None:
        for key, value in params.items():
            name = f"{self.path}/{key}"
            response = self.ssm_client.put_parameter(Name=name, Value=value, Type="SecureString", Overwrite=overwrite)
            print(f"Posted {name} -- version {response['Version']}")

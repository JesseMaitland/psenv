from dataclasses import dataclass
from typing import Optional, Iterator, Dict, Any
from mypy_boto3_ssm import SSMClient

import boto3


@dataclass()
class Parameter:
    name: str
    value: str
    version: int
    kind: str

    @classmethod
    def from_boto3_response(cls, response: Dict[str, Any]) -> "Parameter":
        return cls(
            name=response["Name"],
            value=response["Value"],
            version=response["Version"],
            kind=response["Type"]
        )

    @property
    def parameter_env_key(self) -> str:
        return self.name.split("/")[-1].upper()

    def as_dict(self) -> Dict[str, str]:
        return {self.parameter_env_key: self.value}

class ParameterStoreService:

    def __init__(self, path: str, decrypt: bool, ssm_client: Optional[SSMClient] = None) -> None:
        self._path = path
        self._decrypt = decrypt
        self._ssm_client = ssm_client or boto3.client("ssm")

    @property
    def path(self) -> str:
        return self._path

    @property
    def decrypt(self) -> bool:
        return self._decrypt

    @property
    def ssm_client(self) -> SSMClient:
        return self._ssm_client

    @property
    def fetch_kwargs(self) -> Dict[str, str]:
        return {
            "Path": self.path,
            "WithDecryption": self.decrypt,
            "Recursive": True
        }

    def parameters(self) -> Iterator[Parameter]:
        paginator = self.ssm_client.get_paginator("get_parameters_by_path")
        for response in paginator.paginate(**self.fetch_kwargs):
            for parameter in response["Parameters"]:
                yield Parameter.from_boto3_response(parameter)

    def parameters_as_dict(self) -> Dict[str, str]:
        params = {}
        for parameter in self.parameters():
            params.update(parameter.as_dict())
        return params

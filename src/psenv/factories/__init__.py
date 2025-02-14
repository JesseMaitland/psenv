from typing import List, Iterator
from psenv.core import configs, aws

class ParameterFactory:

    def __init__(self, environments: List[str], decrypt: bool):
        self.environments = environments
        self.decrypt = decrypt

    def api_configs(self) -> Iterator[configs.ApiConfig]:
        for env in self.environments:
            yield configs.ApiConfigLoader(env).load()

    def ssm_services(self) -> Iterator[aws.ParameterStoreService]:
        for api_config in self.api_configs():
            yield aws.ParameterStoreService(
                path=api_config.ssm_path,
                decrypt=self.decrypt
            )

    def parameters(self) -> Iterator[aws.Parameter]:
        for ssm_service in self.ssm_services():
            yield from ssm_service.parameters()

    def list_parameters(self) -> List[aws.Parameter]:
        return list(self.parameters())

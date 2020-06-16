from typing import Dict, List

from py_headless_daw.project.parameter import Parameter


class HavingParameters:
    def __init__(self):
        self._parameters: Dict[str, Parameter] = {}

    def has_parameter(self, name: str) -> bool:
        return name in self._parameters

    def add_parameter(self, name: str, value: float):

        if name in self._parameters:
            raise Exception('parameter named ' + name + ' already added to this object')

        parameter = Parameter(name, value)
        self._parameters[name] = parameter

    def get_parameter(self, name: str) -> Parameter:
        for parameter in self.parameters:
            if parameter.name == name:
                return parameter

        raise Exception('parameter named ' + name + ' not found')

    def get_parameter_value(self, name: str) -> float:
        param = self.get_parameter(name)
        return param.value

    def set_parameter_value(self, name: str, value: float):
        param = self.get_parameter_value(name)
        param.value = value

    @property
    def parameters(self) -> List[Parameter]:
        return list(self._parameters.values())

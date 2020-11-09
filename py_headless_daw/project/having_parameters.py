from typing import Dict, List, cast, Union, Tuple

from py_headless_daw.project.parameter import Parameter


class HavingParameters:

    def __init__(self):
        self._parameters: Dict[str, Parameter] = {}
        super().__init__()

    def has_parameter(self, name: str) -> bool:
        return name in self._parameters

    def add_parameter(self,
                      name: str,
                      value: Union[float, str],
                      param_type: str,
                      value_range: Union[Tuple[float, float], List[str]]):

        if name in self._parameters:
            raise Exception('parameter named ' + name + ' already added to this object')

        parameter = Parameter(name, value, param_type, value_range)
        self._parameters[name] = parameter

    def get_parameter(self, name: str) -> Parameter:
        for parameter in self.parameters:
            if parameter.name == name:
                return parameter

        list_of_names: List[str] = [p.name for p in self.parameters]

        # noinspection PyTypeChecker
        available_names: List[str] = cast(List[str], list_of_names)

        raise Exception('parameter named ' + name + ' not found. Available: ' + ', '.join(available_names))

    def get_parameter_value(self, name: str) -> float:
        param = self.get_parameter(name)
        return param.value

    def set_parameter_value(self, name: str, value: float):
        param = self.get_parameter(name)
        param.value = value

    @property
    def parameters(self) -> List[Parameter]:
        return list(self._parameters.values())

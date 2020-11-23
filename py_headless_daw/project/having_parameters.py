from typing import Dict, List, cast

from py_headless_daw.project.parameter import Parameter, ParameterValueType, ParameterRangeType


class HavingParameters:

    def __init__(self):
        self._parameters: Dict[str, Parameter] = {}
        super().__init__()

    def has_parameter(self, name: str) -> bool:
        return name in self._parameters

    def add_parameter(self,
                      name: str,
                      value: ParameterValueType,
                      param_type: str,
                      value_range: ParameterRangeType):

        if name in self._parameters:
            raise Exception('parameter named ' + name + ' already added to this object')

        parameter = Parameter(name, value, param_type, value_range)
        self._parameters[name] = parameter

    def add_parameter_object(self, parameter: Parameter) -> None:
        self._parameters[parameter.name] = parameter

    def get_parameter(self, name: str) -> Parameter:
        for parameter in self.parameters:
            if parameter.name == name:
                return parameter

        list_of_names: List[str] = [p.name for p in self.parameters]

        # noinspection PyTypeChecker
        available_names: List[str] = cast(List[str], list_of_names)

        raise Exception('parameter named ' + name + ' not found. Available: ' + ', '.join(available_names))

    def get_parameter_value(self, name: str) -> ParameterValueType:
        param = self.get_parameter(name)
        return param.value

    def get_float_parameter_value(self, name: str) -> float:
        param = self.get_parameter(name)
        if param.type != Parameter.TYPE_FLOAT:
            raise ValueError(f"parameter {name} was expected to be float (error: f009d0ef)")
        value = self.get_parameter_value(name)
        cast_value = cast(float, value)
        return cast_value

    def get_enum_parameter_value(self, name: str) -> str:
        param = self.get_parameter(name)
        if param.type != Parameter.TYPE_ENUM:
            raise ValueError(f"parameter {name} was expected to be enum (error: 80a1d180)")
        value = self.get_parameter_value(name)
        cast_value = cast(str, value)
        return cast_value

    def set_parameter_value(self, name: str, value: ParameterValueType):
        param = self.get_parameter(name)
        param.value = value

    @property
    def parameters(self) -> List[Parameter]:
        return list(self._parameters.values())

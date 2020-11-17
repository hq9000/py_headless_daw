from typing import List, Tuple, Union, cast

from py_headless_daw.project.value_provider_consumer import ValueConsumer

ParameterRangeType = Union[Tuple[float, float], List[str]]
ParameterValueType = Union[float, str]


class Parameter(ValueConsumer):
    TYPE_FLOAT = 'float'
    TYPE_ENUM = 'enum'

    def __init__(self, name: str, value: ParameterValueType, parameter_type: str,
                 parameter_range: ParameterRangeType):
        super().__init__()
        self.name: str = name
        if parameter_type not in self.get_available_types():
            raise ValueError(
                f"unsupported parameter type {parameter_type}, supported: {', '.join(self.get_available_types())}")

        self.type: str = parameter_type
        self.range = parameter_range
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value: ParameterValueType):
        if self.type == self.TYPE_FLOAT:
            value_range = cast('Tuple[float, float]', self.range)
            new_value = cast(float, new_value)

            if not isinstance(new_value, float) and not isinstance(new_value, int):
                raise ValueError(
                    f"a new value for parameter {self.name} should have been float, "
                    f"instead is {str(type(new_value))} with value {str(new_value)} (error: 90a2a0ed)")

            if not value_range[0] <= new_value <= value_range[1]:
                raise ValueError(f"float parameter {self.name} value of {new_value} "
                                 f"is out of range {value_range[0]} - {value_range[1]} "
                                 f"(error: 8e343a6e)")

        elif self.type == self.TYPE_ENUM:
            casted_value_range = cast(List[str], self.range)
            if type(new_value) is not str:
                raise ValueError(
                    f"a new value for parameter {self.name} should have been str, "
                    f"instead is {str(type(new_value))} (error: 90a2a0ed)")

            if new_value not in casted_value_range:

                raise ValueError(
                    f"{new_value}, a value for parameter {self.name} should have been one of {', '.join(casted_value_range)}")

        self._value: ParameterValueType = new_value

    @classmethod
    def get_available_types(cls) -> List[str]:
        return [cls.TYPE_FLOAT, cls.TYPE_ENUM]

    @property
    def range(self) -> ParameterRangeType:
        return self._range

    @range.setter
    def range(self, value: ParameterValueType):
        if self.type == self.TYPE_FLOAT:
            if isinstance(value, tuple):
                if len(value) != 2:
                    raise ValueError('ranges for float params must be tuples of length 2 (error: a27c90e2)')
                for i in range(2):
                    if not isinstance(value[i], float) and not isinstance(value[i], int):
                        raise ValueError('ranges for float params must be tuples of floats or ints (error: 80d5db89)')
            else:
                raise ValueError('for float params, range must be a tuple of two floats (error: e37e6f14)')
        elif self.type == self.TYPE_ENUM:
            if isinstance(value, list):
                for e in value:
                    if not isinstance(e, str):
                        raise ValueError('for enum params, each element range must be a string (error: f0dc465c)')
            else:
                raise ValueError('for enum params, range must be a list of strings (error: a9c603f3)')
        else:
            raise ValueError('unsupported type (error: 2878e15c)')

        self._range: ParameterRangeType = value

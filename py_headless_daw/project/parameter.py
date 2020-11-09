from typing import List, Tuple, Union, cast

from py_headless_daw.project.value_provider_consumer import ValueConsumer


class Parameter(ValueConsumer):
    TYPE_FLOAT = 'float'
    TYPE_ENUM = 'enum'

    def __init__(self, name: str, value: Union[float, str], parameter_type: str,
                 parameter_range: Union[Tuple[float, float], List[str]]):
        super().__init__()
        self.name: str = name
        self.value: Union[float, str] = value
        self.type: str = parameter_type
        self.range = parameter_range

    @property
    def value(self):
        return self.value

    @value.setter
    def value(self, new_value: Union[float, str]):
        if self.type == self.TYPE_FLOAT:
            value_range = cast(self.range, Tuple[float, float])
            value = cast(new_value, float)

            if type(value) is not float:
                raise ValueError(
                    f"a new value for parameter {self.name} should have been float, "
                    f"instead is {str(type(new_value))} (error: 90a2a0ed)")

            if not value_range[0] <= new_value <= value_range[1]:
                raise ValueError(f"float parameter {self.name} value of {new_value} "
                                 f"is out of range {value_range[0]} - {value_range[1]} "
                                 f"(error: 8e343a6e)")

            self.value = new_value
        elif self.type == self.TYPE_ENUM:
            value_range = cast(self.range, List[str])
            if type(new_value) is not str:
                raise ValueError(
                    f"a new value for parameter {self.name} should have been str, "
                    f"instead is {str(type(new_value))} (error: 90a2a0ed)")

            if new_value not in value_range:
                raise ValueError(
                    f"{new_value}, a value for parameter {self.name} should have been one of {', '.join(value_range)}")

            self.value = new_value

from typing import List

from py_headless_daw.project.parameter import Parameter
from py_headless_daw.project.value_provider_consumer import ValueProvider


class EnvelopePoint:
    SLOPE_TYPE_LINEAR = 'linear'
    SLOPE_TYPE_QUADRATIC = 'quadratic'
    SLOPE_TYPE_SPLINE = 'spline'

    def __init__(self, time: float):
        self.time: float = time

        self.left_slope_type: str = self.SLOPE_TYPE_LINEAR
        self.left_slope_parameter: float = 1.1

        self.right_slope_type: str = self.SLOPE_TYPE_LINEAR
        self.right_slope_parameter: float = 1.1


class Envelope(ValueProvider):

    def __init__(self, parameter: Parameter):
        super().__init__()
        self.target: Parameter = parameter
        self.points: List[EnvelopePoint] = []

    def get_value(self, time: float) -> float:
        return 0.5

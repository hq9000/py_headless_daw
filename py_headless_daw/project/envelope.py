from typing import List

from py_headless_daw.project.parameter import Parameter


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


class Envelope:
    def __init__(self, parameter: Parameter):
        self.target: Parameter = parameter
        self.points: List[EnvelopePoint] = []

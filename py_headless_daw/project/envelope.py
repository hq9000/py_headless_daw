from typing import List

from py_headless_daw.project.value_provider_consumer import ValueProvider, ValueConsumer


class EnvelopePoint:
    SLOPE_TYPE_LINEAR = 'linear'
    SLOPE_TYPE_QUADRATIC = 'quadratic'
    SLOPE_TYPE_SPLINE = 'spline'

    def __init__(self, time: float, value: float):
        self.time: float = time
        self.value: float = value

        self.left_slope_type: str = self.SLOPE_TYPE_LINEAR
        self.left_slope_parameter: float = 1.1

        self.right_slope_type: str = self.SLOPE_TYPE_LINEAR
        self.right_slope_parameter: float = 1.1


class Envelope(ValueProvider):

    def __init__(self, value_consumer: ValueConsumer):
        super().__init__()
        self.target: ValueConsumer = value_consumer
        self.target.value_provider = self
        self._points: List[EnvelopePoint] = []

    @property
    def points(self) -> List[EnvelopePoint]:
        return self._points

    @points.setter
    def points(self, points: List[EnvelopePoint]):
        self._points = sorted(points, key=lambda point: point.time)

    def get_value(self, time: float) -> float:
        if time <= self._points[0].time:
            return self._points[0].value
        elif time >= self._points[-1].time:
            return self._points[-1].value

        for idx in range(0, len(self._points) - 1):

            prev_time: float = self._points[idx].time
            next_time: float = self._points[idx + 1].time

            prev_value: float = self._points[idx].value
            next_value: float = self._points[idx + 1].value

            if prev_time <= time < next_time:
                return prev_value + (next_value - prev_value) * (time - prev_time) / (next_time - prev_time)

        raise Exception('unable to find a range')

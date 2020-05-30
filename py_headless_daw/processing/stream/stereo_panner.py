from typing import List

import numpy as np

from py_headless_daw.schema.dto.time_interval import TimeInterval
from py_headless_daw.schema.events.event import Event
from py_headless_daw.schema.processing_strategy import ProcessingStrategy


class StereoPanner(ProcessingStrategy):

    def __init__(self, panning: float):
        super().__init__()
        self.panning = panning

    def render(self, interval: TimeInterval, stream_inputs: List[np.ndarray], stream_outputs: List[np.ndarray],
               event_inputs: List[List[Event]], event_outputs: List[List[Event]]):
        left_gain: float = self._get_left_gain(self.panning)
        right_gain: float = self._get_right_gain(self.panning)

        for i in range(0, len(stream_inputs)):
            np.copyto(stream_outputs[i], stream_inputs[i])

        stream_outputs[0] *= left_gain
        stream_outputs[1] *= right_gain

    def _get_left_gain(self, gain: float):
        if gain < 0:
            return 1

        return 1 - gain

    def _get_right_gain(self, gain: float):
        if gain > 0:
            return 1

        return gain + 1.0

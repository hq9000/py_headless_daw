from typing import List, Dict

import numpy as np

from em.platform.rendering.dto.time_interval import TimeInterval
from em.platform.rendering.schema.events.event import Event
from em.platform.rendering.schema.processing_strategy import ProcessingStrategy


class Mixer(ProcessingStrategy):

    def __init__(self):
        self.gains: Dict[int, float] = {}
        self.pannings: Dict[int, float] = {}

    def set_gain(self, track_number: int, gain: float):
        self.gains[track_number] = gain

    def get_gain(self, track_number: int):
        return self.gains[track_number]

    def set_panning(self, track_number: int, panning: float):
        self.pannings[track_number] = panning

    def render(self, interval: TimeInterval, stream_inputs: List[np.ndarray], stream_outputs: List[np.ndarray],
               event_inputs: List[List[Event]], event_outputs: List[List[Event]]):

        num_input_stream_channels: int = len(stream_inputs)
        num_output_stream_channels: int = len(stream_outputs)

        for stream_output in stream_outputs:
            stream_output.fill(0.0)

        # assuming each unit provides the same number of channels to the mixer,
        # if it doesn't, everything will break
        num_input_units: int = int(num_input_stream_channels / num_output_stream_channels)
        for u in range(0, num_input_units):

            base_gain: float = self._get_gain(u)
            panning: float = self._get_panning(u)

            left_gain: float = base_gain * (1 - max([0, panning]))
            right_gain: float = base_gain * (1 + min([0, panning]))

            stream_outputs[0] += left_gain * stream_inputs[u * num_output_stream_channels + 0]
            stream_outputs[1] += right_gain * stream_inputs[u * num_output_stream_channels + 1]

    def _get_gain(self, u) -> float:
        if u in self.gains:
            return self.gains[u]
        else:
            return 1.0

    def _get_panning(self, u) -> float:
        if u in self.pannings:
            return self.pannings[u]
        else:
            return 0.0

from typing import List

import numpy as np

from py_headless_daw.schema.dto.time_interval import TimeInterval
from py_headless_daw.schema.events.event import Event
from py_headless_daw.schema.processing_strategy import ProcessingStrategy


class Transparent(ProcessingStrategy):
    def render(self, interval: TimeInterval, stream_inputs: List[np.ndarray], stream_outputs: List[np.ndarray],
               event_inputs: List[List[Event]], event_outputs: List[List[Event]]):
        if len(stream_inputs) != len(stream_outputs):
            raise Exception(
                'it was expected that the number of output stream'
                ' channels is the same as number of input stream channels')

        if len(event_inputs) != len(event_outputs):
            raise Exception(
                'it was expected that the number of output event channels is the same as number of input event channels')

        for i, stream_input in enumerate(stream_inputs):
            np.copyto(stream_outputs[i], stream_input)

        for i, event_input in enumerate(event_inputs):
            for event in event_input:
                event_outputs[i].append(event)

        pass

from typing import List

import numpy as np
import random

from py_headless_daw.schema.dto.time_interval import TimeInterval
from py_headless_daw.schema.events.event import Event
from py_headless_daw.schema.processing_strategy import ProcessingStrategy


class ImpulseNoiseGeneratorStrategy(ProcessingStrategy):
    """
    generates portions of noise intermittenly with portions of silence.
    Used mainly for testing and initial development.
    """

    def __init__(self):
        super().__init__()
        self.times_called = 0

    def render(self, interval: TimeInterval, stream_inputs: List[np.ndarray], stream_outputs: List[np.ndarray],
               event_inputs: List[List[Event]], event_outputs: List[List[Event]]):

        num_samples = stream_outputs[0].shape[0]

        for i in range(0, num_samples):
            if i < num_samples // 2 and self.times_called < 2:
                for output in stream_outputs:
                    output[i] = random.uniform(-1, 1)
            else:
                for output in stream_outputs:
                    output[i] = .0

        self.times_called += 1

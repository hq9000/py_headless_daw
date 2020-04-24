from typing import List

import numpy as np
import random

from py_headless_daw.schema.dto.time_interval import TimeInterval
from py_headless_daw.schema.events.event import Event
from py_headless_daw.schema.processing_strategy import ProcessingStrategy


class ImpulseNoiseGeneratorStrategy(ProcessingStrategy):

    def __init__(self):
        self.times_called = 0

    def render(self, interval: TimeInterval, stream_inputs: List[np.ndarray], stream_outputs: List[np.ndarray],
               event_inputs: List[List[Event]], event_outputs: List[List[Event]]):

        num_samples = stream_outputs[0].shape[0]

        for i in range(0, num_samples):
            if i < num_samples // 2 and self.times_called < 2:
                stream_outputs[0][i] = random.uniform(-1, 1)
                stream_outputs[1][i] = random.uniform(-1, 1)
            else:
                stream_outputs[0][i] = .0
                stream_outputs[1][i] = .0

        self.times_called += 1

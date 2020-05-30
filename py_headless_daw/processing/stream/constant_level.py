from typing import List

import numpy as np

from py_headless_daw.schema.dto.time_interval import TimeInterval
from py_headless_daw.schema.events.event import Event
from py_headless_daw.schema.processing_strategy import ProcessingStrategy


class ConstantLevel(ProcessingStrategy):

    def __init__(self, level: np.float32):
        super().__init__()
        self.level: np.float32 = level

    def render(self, interval: TimeInterval, stream_inputs: List[np.ndarray], stream_outputs: List[np.ndarray],
               event_inputs: List[List[Event]], event_outputs: List[List[Event]]):
        for buffer in stream_outputs:
            buffer.fill(self.level)

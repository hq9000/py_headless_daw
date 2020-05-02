from typing import List

import numpy as np

from py_headless_daw.schema.dto.time_interval import TimeInterval
from py_headless_daw.schema.events.event import Event
from py_headless_daw.schema.processing_strategy import ProcessingStrategy


class ConstantLevel(ProcessingStrategy):

    def __init__(self, level: np.float32):
        self.level: np.float32 = level

    def render(self, interval: TimeInterval, stream_inputs: np.ndarray, stream_outputs: np.ndarray,
               event_inputs: List[List[Event]], event_outputs: List[List[Event]]):
        stream_outputs.fill(self.level)

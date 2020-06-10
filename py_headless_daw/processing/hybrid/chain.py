from typing import List

import numpy as np

from py_headless_daw.schema.dto.time_interval import TimeInterval
from py_headless_daw.schema.events.event import Event
from py_headless_daw.schema.processing_strategy import ProcessingStrategy
from py_headless_daw.schema.unit import Unit


class Chain(ProcessingStrategy):

    def __init__(self, input_unit: Unit, output_unit: Unit):
        super().__init__()
        self.input_unit = input_unit
        self.output_unit = output_unit
        pass

    def render(self, interval: TimeInterval, stream_inputs: List[np.ndarray], stream_outputs: List[np.ndarray],
               event_inputs: List[List[Event]], event_outputs: List[List[Event]]):
        todo

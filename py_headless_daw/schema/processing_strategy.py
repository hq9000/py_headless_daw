from abc import abstractmethod, ABC
from typing import List, Optional

import numpy as np

from py_headless_daw.schema.dto.time_interval import TimeInterval
from py_headless_daw.schema.events.event import Event
from py_headless_daw.schema.unit import Unit


class ProcessingStrategy(ABC):

    def __init__(self):
        self._unit: Optional[Unit] = None

    @abstractmethod
    def render(self, interval: TimeInterval, stream_inputs: List[np.ndarray], stream_outputs: List[np.ndarray],
               event_inputs: List[List[Event]], event_outputs: List[List[Event]]):
        pass

    @property
    def unit(self) -> Optional[Unit]:
        return self._unit

    @unit.setter
    def unit(self, unit: Unit):
        self._unit = unit

    @staticmethod
    def _flatten_event_inputs(event_inputs: List[List[Event]]) -> List[Event]:

        events: List[Event] = []

        # we gather all midi events from all event inputs
        for event_input in event_inputs:
            for event in event_input:
                events.append(event)

        return events

    def _filter_events(self, event_inputs: List[List[Event]], event_type: str) -> List[Event]:
        flattened_events: List[Event] = self._flatten_event_inputs(event_inputs)

        res = []
        for event in flattened_events:
            if event.type == event_type:
                res.append(event)

        return res

from typing import List

import numpy as np

from em.platform.rendering.dto.time_interval import TimeInterval
from em.platform.rendering.schema.events.event import Event
from em.platform.rendering.schema.processing_strategy import ProcessingStrategy


class EventBuffer(ProcessingStrategy):

    def render(self, interval: TimeInterval, stream_inputs: List[np.ndarray], stream_outputs: List[np.ndarray],
               event_inputs: List[List[Event]], event_outputs: List[List[Event]]):

        # this strategy just copies its buffer to all event outputs its node has
        for event in self._events:
            for output in event_outputs:
                output.append(event)

    def __init__(self):
        self._events: List[Event] = []

    def give_new_events(self, events: List[Event]):
        self._events = events

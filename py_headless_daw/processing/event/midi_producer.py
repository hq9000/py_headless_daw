from typing import List

import numpy as np

from em.platform.rendering.dto.time_interval import TimeInterval
from em.platform.rendering.schema.events.event import Event
from em.platform.rendering.schema.events.midi_event import MidiEvent

from em.platform.rendering.schema.processing_strategy import ProcessingStrategy


class MidiProducer(ProcessingStrategy):

    def __init__(self, events: List[MidiEvent]):
        self._events = events

    def render(self, interval: TimeInterval, stream_inputs: List[np.ndarray], stream_outputs: List[np.ndarray],
               event_inputs: List[List[Event]], event_outputs: List[List[Event]]):
        for event in self._events:
            for output in event_outputs:
                output.append(event)

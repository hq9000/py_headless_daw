import random
from typing import List

import numpy as np

from em.platform.rendering.arrangement.globally_positioned_event import GloballyPositionedEvent
from em.platform.rendering.dto.time_interval import TimeInterval
from em.platform.rendering.schema.events.event import Event
from em.platform.rendering.schema.processing_strategy import ProcessingStrategy


class EventTrack(ProcessingStrategy):

    def __init__(self, events: List[GloballyPositionedEvent]):
        sorted_events = sorted(events, key=lambda k: k.position_in_bars)
        self._events: List[GloballyPositionedEvent] = sorted_events
        self._random = random.Random()

    def render(self, interval: TimeInterval, stream_inputs: List[np.ndarray], stream_outputs: List[np.ndarray],
               event_inputs: List[List[Event]], event_outputs: List[List[Event]]):

        for event in self._events:
            if interval.start_in_bars <= event.position_in_bars < interval.end_in_bars:
                sample_position = interval.num_samples * (event.position_in_bars - interval.start_in_bars) / interval.get_length_in_bars()

                sample_position: int = round(sample_position)
                real_event = event.event
                real_event.sample_position = sample_position
                dice = self._random.uniform(0, 1)
                if dice < real_event.probability:
                    event_outputs[0].append(real_event)

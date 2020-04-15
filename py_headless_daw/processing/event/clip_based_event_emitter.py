from typing import List

import numpy as np

from em.platform.rendering.arrangement.event_clip import EventClip
from em.platform.rendering.arrangement.event_clip_buffer_mapper import EventClipBufferMapper
from em.platform.rendering.dto.time_interval import TimeInterval
from em.platform.rendering.schema.events.event import Event

from em.platform.rendering.schema.processing_strategy import ProcessingStrategy


class ClipBasedEventEmitter(ProcessingStrategy):

    def __init__(self):
        self.clip: EventClip = None
        self._mapper: EventClipBufferMapper = EventClipBufferMapper()

    def render(self, interval: TimeInterval, stream_inputs: List[np.ndarray], stream_outputs: List[np.ndarray],
               event_inputs: List[List[Event]], event_outputs: List[List[Event]]):

        events: List[Event] = self.generateEvents(interval)

        for event in events:
            if event.should_happen():
                for output in event_outputs:
                    output.append(event)

    def generateEvents(self, interval: TimeInterval) -> List[Event]:
        return self._mapper.map_event_clip_to_buffer(self.clip, interval.num_samples, interval.start_in_bars,
                                                     interval.end_in_bars)

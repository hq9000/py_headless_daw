from abc import ABC, abstractmethod
from typing import List
import numpy as np

from em.platform.rendering.dto.time_interval import TimeInterval
from em.platform.rendering.schema.events.event import Event
from em.platform.rendering.schema.processing_strategy import ProcessingStrategy


class AbstractStatelessEventProcessor(ProcessingStrategy, ABC):

    # noinspection PyUnusedLocal
    def render(self, interval: TimeInterval, stream_inputs: List[np.ndarray], stream_outputs: List[np.ndarray],
               event_inputs: List[List[Event]], event_outputs: List[List[Event]]):
        for i in range(0, len(event_inputs)):
            for e in event_inputs[i]:
                self._process_event(e, interval.num_samples)
                event_outputs[i].append(e)

    @abstractmethod
    def _process_event(self, e: Event, buffer_length: int):
        pass

from typing import List, Callable

import numpy as np

from py_headless_daw.project.value_provider_consumer import ValueProvider
from py_headless_daw.schema.dto.time_interval import TimeInterval
from py_headless_daw.schema.events.event import Event
from py_headless_daw.schema.processing_strategy import ProcessingStrategy


class ValueProviderBasedEventEmitter(ProcessingStrategy):
    DEFAULT_SAMPLING_PERIOD = 0.05

    def __init__(self, provider: ValueProvider, transformer: Callable[[float, int], Event],
                 sampling_period=DEFAULT_SAMPLING_PERIOD):
        super().__init__()
        self._provider: ValueProvider = provider
        self._transformer_function: Callable[[float, int], Event] = transformer
        self._sampling_period = sampling_period

    def render(self, interval: TimeInterval, stream_inputs: List[np.ndarray], stream_outputs: List[np.ndarray],
               event_inputs: List[List[Event]], event_outputs: List[List[Event]]):
        # warning! dummy implementation, to be refined
        # it's just emitting an event in the beginning of every block
        value: float = self._provider.get_value(interval.start_in_seconds)
        event: Event = self._transformer_function(value, 0)
        event_outputs[0].append(event)

from typing import List

import numpy as np

from em.platform.rendering.dto.time_interval import TimeInterval
from em.platform.rendering.primitives.envelope import Envelope
from em.platform.rendering.schema.events.event import Event
from em.platform.rendering.schema.events.parameter_value_event import ParameterValueEvent
from em.platform.rendering.schema.processing_strategy import ProcessingStrategy


class EnvelopeParamValueEmitter(ProcessingStrategy):

    def __init__(self, envelope: Envelope, parameter: str):
        self.envelope: Envelope = envelope
        self.parameter: str = parameter

    def render(self, interval: TimeInterval, stream_inputs: List[np.ndarray], stream_outputs: List[np.ndarray],
               event_inputs: List[List[Event]], event_outputs: List[List[Event]]):
        # a simplified approach:
        # only one event is generated, in the very beginning of buffer
        # must be good enough for the beginning
        event = ParameterValueEvent(0, self.parameter, self.envelope.get_value_at(interval.start_in_bars))
        for output in event_outputs:
            output.append(event)

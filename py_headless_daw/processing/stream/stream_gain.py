from typing import List, cast

import numpy as np

from py_headless_daw.schema.dto.time_interval import TimeInterval
from py_headless_daw.schema.events.event import Event
from py_headless_daw.schema.events.parameter_value_event import ParameterValueEvent
from py_headless_daw.schema.processing_strategy import ProcessingStrategy


class StreamGain(ProcessingStrategy):
    PARAMETER_GAIN: str = 'gain'

    def __init__(self, gain: np.float32):
        self.gain: np.float32 = gain
        super().__init__()

    # noinspection PyShadowingNames
    def render(self, interval: TimeInterval, stream_inputs: List[np.ndarray], stream_outputs: List[np.ndarray],
               event_inputs: List[List[Event]], event_outputs: List[List[Event]]):

        # simplified approach:
        # we check all events arrived and react on any param value events,
        # the last one we face will determine current gain value, if none have arrived,
        # the gain will not change
        all_events = self._flatten_event_inputs(event_inputs)
        all_events = sorted(all_events, key=lambda event: event.sample_position)

        new_desired_gain = self.gain

        for event in all_events:
            if isinstance(event, ParameterValueEvent):
                event = cast(ParameterValueEvent, event)
                if event.parameter_id == self.PARAMETER_GAIN:
                    new_desired_gain = event.value

        if new_desired_gain != self.gain:
            # even in this simplified approach,
            # we still want to avoid abrupt volume changes resulting in clicks,
            # for that we smoothen out transition:
            # if a change in gain is detected (new desired gain != current gain),
            # it will be reached during this buffer by applying a slowly changing array
            gain_operation = self._get_smoothener_array(self.gain, new_desired_gain, stream_outputs[0].shape[0])
        else:
            gain_operation = self.gain

        self.gain = new_desired_gain

        for i in range(0, len(stream_inputs)):
            np.copyto(stream_outputs[i], stream_inputs[i])
            stream_outputs[i] *= gain_operation

    def _get_smoothener_array(self, initial_gain: float, new_desired_gain: float, num_samples: int) -> np.ndarray:
        return np.linspace(start=initial_gain, stop=new_desired_gain, num=num_samples, dtype=np.float32)

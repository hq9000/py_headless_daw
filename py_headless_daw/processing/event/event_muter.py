from typing import List

import numpy as np

from em.platform.common.mixins.fuzzily_deterministic_object import FuzzilyDeterministicObject
from em.platform.common.random_decider import RandomDecider
from em.platform.rendering.dto.time_interval import TimeInterval
from em.platform.rendering.schema.events.event import Event
from em.platform.rendering.schema.processing_strategy import ProcessingStrategy


class EventMuter(ProcessingStrategy, FuzzilyDeterministicObject):

    def __init__(self, seed):
        super().__init__()
        self.pass_probability: float = None
        self.block_probability: float = None
        self.num_bars_decision_is_valid: int = None
        self._last_bar_decision_made: int = None
        self._last_bar_decision: bool = None
        self.seed(seed)

    def render(self, interval: TimeInterval, stream_inputs: List[np.ndarray], stream_outputs: List[np.ndarray],
               event_inputs: List[List[Event]], event_outputs: List[List[Event]]):

        for input_number in range(0, len(event_inputs)):
            for event in event_inputs[input_number]:
                if self._event_should_pass(event, interval):
                    event_outputs[input_number].append(event)

    def _event_should_pass(self, event: Event, interval: TimeInterval) -> bool:

        if event.get_type() == Event.TYPE_MIDI:
            # noinspection PyUnresolvedReferences
            if event.is_note_off():
                return True

        event_bar_position: float = self._get_bar_position(event.sample_position, interval)
        bar_number: int = np.floor(event_bar_position)
        return self._is_passing_at_bar(bar_number)

    def _is_passing_at_bar(self, bar_number: int) -> bool:
        if self._last_bar_decision_made is not None:
            if self._last_bar_decision_made <= bar_number < self._last_bar_decision_made \
                    + self.num_bars_decision_is_valid:
                return self._last_bar_decision

        self._last_bar_decision = self._generate_new_decision()
        self._last_bar_decision_made = bar_number

        return self._last_bar_decision

    def _generate_new_decision(self) -> bool:
        decider = RandomDecider()
        return decider.decide(self.get_random_generator(), {
            True: self.pass_probability,
            False: self.block_probability
        })

    def _get_bar_position(self, sample_position: int, interval: TimeInterval) -> float:
        length_of_buffer_bars: float = interval.end_in_bars - interval.start_in_bars
        return interval.start_in_bars + sample_position / interval.num_samples * length_of_buffer_bars

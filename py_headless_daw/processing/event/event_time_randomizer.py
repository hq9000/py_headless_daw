from em.platform.common.mixins.fuzzily_deterministic_object import FuzzilyDeterministicObject
from em.platform.rendering.processing_strategies.event.abc.abstract_stateless_event_processor import AbstractStatelessEventProcessor
from em.platform.rendering.schema.events.event import Event


class EventTimeRandomizer(FuzzilyDeterministicObject, AbstractStatelessEventProcessor):

    def __init__(self, seed):
        super().__init__()
        self.randomness_in_samples: int = 100

    def _process_event(self, e: Event, buffer_length: int):
        shift = round(
            self.get_random_generator().randrange(-0.5 * self.randomness_in_samples, 0.5 * self.randomness_in_samples))
        new_position = e.sample_position + shift
        if new_position < 0:
            new_position = 0

        if new_position > buffer_length - 1:
            new_position = buffer_length - 1

        e.sample_position = new_position

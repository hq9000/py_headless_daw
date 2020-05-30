from abc import abstractmethod, ABC
import random


class Event(ABC):

    TYPE_MIDI = 'midi'
    TYPE_TRACK_SAMPLER = 'track_sampler'
    TYPE_PARAMETER_VALUE = 'param_value'

    @property
    @abstractmethod
    def type(self):
        pass

    def __init__(self, sample_position: int):
        self.sample_position: int = sample_position
        self.probability: float = 1.0

    def get_sample_position(self) -> int:
        return self.sample_position

    def should_happen(self) -> bool:
        return random.uniform(0.0, 1.0) < self.probability

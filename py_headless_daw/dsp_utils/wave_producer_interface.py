from abc import ABC, abstractmethod
import numpy as np


class WaveProducerInterface(ABC):

    @abstractmethod
    def render_to_buffer(self, output_buffer: np.ndarray, sample_rate: int, start_sample: int):
        pass


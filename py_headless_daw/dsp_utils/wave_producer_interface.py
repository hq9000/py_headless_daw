from abc import ABC, abstractmethod
import numpy as np


class WaveProducerInterface(ABC):
    MODE_REPLACE = 'replace'
    MODE_MIX = 'mix'

    @abstractmethod
    def render_to_buffer(self, output_buffer: np.ndarray, sample_rate: int, start_sample: int, mode: str = MODE_REPLACE):
        pass

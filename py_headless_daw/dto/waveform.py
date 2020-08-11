import numpy as np


class Waveform:
    def __init__(self, sample_rate: int, data: np.ndarray):
        self.sample_rate: int = sample_rate
        self.data: np.ndarray = data
        pass

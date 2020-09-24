import numpy as np  # type: ignore


class Waveform:
    def __init__(self, sample_rate: int, data: np.ndarray):
        self.sample_rate: int = sample_rate
        self.data: np.ndarray = data
        pass

    def length_in_samples(self) -> int:
        return self.data.shape[1]

    @property
    def num_channels(self) -> int:
        return self.data.shape[0]

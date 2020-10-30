import numpy as np

from py_headless_daw.dsp_utils.wave_producer_interface import WaveProducerInterface


# https://en.wikipedia.org/wiki/Envelope_(music)#ADSR
class ADSREnvelope(WaveProducerInterface):

    def __init__(self, attack: float, decay: float, sustain: float, release: float):
        self.attack_time: float = attack
        self.decay_time: float = decay
        self.sustain_level: float = sustain
        self.release_time: float = release

        self.attack_curve: float = 0  # 0 means linear, other values in [-1, 1] range (will) be different extents of curveness
        self.decay_curve: float = 0
        self.release_curve: float = 0

    def produce(self, output_buffer: np.ndarray, sample_rate: int, start_sample: int):
        pass

    def get_value(self, sample: int, sample_rate: int) -> float:
        return 1
        pass

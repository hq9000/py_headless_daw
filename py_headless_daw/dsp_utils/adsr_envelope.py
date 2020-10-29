import numpy as np

from py_headless_daw.dsp_utils.wave_producer_interface import WaveProducerInterface


class ADSREnvelope(WaveProducerInterface):

    def __init__(self, attack: float, decay: float, sustain: float, release: float):
        self.attack: float = attack
        self.decay: float = decay
        self.sustain: float = sustain
        self.release: float = release

    def produce(self, output_buffer: np.ndarray, sample_rate: int, start_sample: int):
        pass

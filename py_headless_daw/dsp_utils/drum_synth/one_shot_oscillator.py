import numpy as np

from py_headless_daw.dsp_utils.adsr_envelope import ADSREnvelope
from py_headless_daw.dsp_utils.wave_producer_interface import WaveProducerInterface


class OneShotOscillator(WaveProducerInterface):
    def produce(self, output_buffer: np.ndarray, sample_rate: int, start_sample: int):

        # 1. generate a volume envelope wave
        # 2. generate a modulated pitch wave (without volume)
        # 3. multiply two above
        # put to output buffer




        pass

    TYPE_SINE: str = "sine"
    TYPE_NOISE: str = "noise"
    TYPE_TRIANGLE: str = "triangle"

    def __init__(self):
        self.pitch_envelope: ADSREnvelope = self._create_default_envelope()
        self.volume_envelope: ADSREnvelope = self._create_default_envelope()
        self.frequency = 440
        self.wave = self.TYPE_SINE

    def _create_default_envelope(self) -> ADSREnvelope:
        return ADSREnvelope(0, 1, 1, 1)

import numpy as np

from py_headless_daw.dsp_utils.adsr_envelope import ADSREnvelope
from py_headless_daw.dsp_utils.wave_producer_interface import WaveProducerInterface


class OneShotOscillator(WaveProducerInterface):
    def produce(self, output_buffer: np.ndarray, sample_rate: int, start_sample: int):

        if output_buffer.ndim != (1,):
            raise ValueError("buffers give to an oscillaltor are supposed to be mono")

        volume_env_wave = np.copy(output_buffer)
        self.volume_envelope.produce(volume_env_wave, sample_rate, start_sample)

        oscillation_wave = np.copy(output_buffer)
        self._generate_oscillation_wave(oscillation_wave, sample_rate, start_sample)

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

    def _generate_oscillation_wave(self, osciallation_wave, sample_rate, start_sample):
        pass

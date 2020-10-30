import numpy as np
import math

from py_headless_daw.dsp_utils.adsr_envelope import ADSREnvelope
from py_headless_daw.dsp_utils.wave_producer_interface import WaveProducerInterface


class OneShotOscillator(WaveProducerInterface):
    TYPE_SINE: str = "sine"
    TYPE_NOISE: str = "noise"
    TYPE_TRIANGLE: str = "triangle"

    def produce(self, output_buffer: np.ndarray, sample_rate: int, start_sample: int):
        if output_buffer.ndim != 1:
            raise ValueError(f"buffers given to an oscillator are supposed to be mono, "
                             f"this one has {output_buffer.ndim} dimensions instead of 1")

        volume_env_wave = np.copy(output_buffer)
        self.volume_envelope.produce(volume_env_wave, sample_rate, start_sample)

        oscillation_wave = np.copy(output_buffer)
        self._generate_oscillation_wave(oscillation_wave, sample_rate, start_sample)

        np.multiply(oscillation_wave, volume_env_wave, out=output_buffer)

    def __init__(self):
        self.pitch_envelope: ADSREnvelope = self._create_default_envelope()
        self.volume_envelope: ADSREnvelope = self._create_default_envelope()
        self.frequency: float = 440.0
        self.wave = self.TYPE_SINE
        self.initial_phase: float = 0.0

    def _create_default_envelope(self) -> ADSREnvelope:
        return ADSREnvelope(0, 1, 1, 1)

    def _generate_oscillation_wave(self, out_buffer: np.ndarray, sample_rate, start_sample):
        phase: float = self.initial_phase
        for i in range(out_buffer.shape[0]):
            frequency = self.pitch_envelope.get_value(start_sample + i, sample_rate)
            out_buffer[i] = math.sin(phase)
            phase += frequency

import numpy as np
import math

from py_headless_daw.dsp_utils.adsr_envelope import ADSREnvelope
from py_headless_daw.dsp_utils.wave_producer_interface import WaveProducerInterface


class OneShotOscillator(WaveProducerInterface):
    # different signals https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.sawtooth.html
    TYPE_SINE: str = "sine"
    TYPE_NOISE: str = "noise"
    TYPE_TRIANGLE: str = "triangle"

    def __init__(self):
        self.pitch_envelope: ADSREnvelope = self._create_default_envelope()
        self.volume_envelope: ADSREnvelope = self._create_default_envelope()
        self.zero_frequency: float = 440.0
        self.frequency_range: float = 440.0
        self.wave = self.TYPE_SINE
        self.distortion: float = 0.0
        self.initial_phase: float = 0.0
        self.volume: float = 1.0

    def render_to_buffer(self, output_buffer: np.ndarray, sample_rate: int, start_sample: int,
                         mode: str = WaveProducerInterface.MODE_REPLACE):

        if output_buffer.ndim != 1:
            raise ValueError(f"buffers given to an oscillator are supposed to be mono, "
                             f"this one has {output_buffer.ndim} dimensions instead of 1")

        volume_env_wave = np.copy(output_buffer)
        self.volume_envelope.render_to_buffer(volume_env_wave, sample_rate, start_sample)

        oscillation_wave = np.copy(output_buffer)
        self._generate_oscillation_wave(oscillation_wave, sample_rate, start_sample)

        np.multiply(oscillation_wave, volume_env_wave, out=oscillation_wave)

        if WaveProducerInterface.MODE_REPLACE == mode:
            np.copyto(output_buffer, oscillation_wave)
        elif WaveProducerInterface.MODE_MIX == mode:
            np.add(output_buffer, oscillation_wave, out=output_buffer)
        else:
            raise ValueError(f'unknown producing mode {mode}')

    def _create_default_envelope(self) -> ADSREnvelope:
        return ADSREnvelope(attack_time=0, decay_time=1, sustain_level=1, sustain_time=0, release_time=1)

    def _generate_oscillation_wave(self, out_buffer: np.ndarray, sample_rate, start_sample):
        phase: float = self.initial_phase
        for i in range(out_buffer.shape[0]):
            relative_frequency = self.pitch_envelope.get_one_value(start_sample + i, sample_rate)
            real_frequency = self.zero_frequency + self.frequency_range * relative_frequency

            out_buffer[i] = self._wave_function(self.wave, self.distortion, phase)

            if real_frequency > 0:
                samples_in_period = (1 / real_frequency) * sample_rate
                oscillator_step_for_one_sample = 2 * math.pi / samples_in_period
                phase += oscillator_step_for_one_sample

    def _wave_function(self, waveform: str, distortion: float, phase: float) -> float:
        return math.sin(phase)

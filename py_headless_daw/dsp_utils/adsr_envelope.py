import numpy as np
import math

from py_headless_daw.dsp_utils.wave_producer_interface import WaveProducerInterface


# https://en.wikipedia.org/wiki/Envelope_(music)#ADSR
class ADSREnvelope(WaveProducerInterface):

    def __init__(self, attack_time: float, decay_time: float, sustain_level: float, sustain_time: float, release_time: float):
        self.attack_time: float = attack_time
        self.decay_time: float = decay_time
        self.sustain_level: float = sustain_level
        self.sustain_time: float = sustain_time
        self.release_time: float = release_time

        self.attack_curve: float = 0  # 0 means linear, other values in [-1, 1] range (will) be different extents of curveness
        self.decay_curve: float = 0
        self.release_curve: float = 0

    def produce(self, output_buffer: np.ndarray, sample_rate: int, start_sample: int):
        for i in range(output_buffer.shape[0]):
            output_buffer[i] = self.get_value(start_sample + i, sample_rate)

    def get_value(self, sample: int, sample_rate: int) -> float:
        end_of_attack_sample: int = round(self.attack_time * sample_rate)
        end_of_decay_sample: int = end_of_attack_sample + round(self.decay_time * sample_rate)
        end_of_sustain_sample: int = end_of_decay_sample + round(self.sustain_time * sample_rate)
        end_of_release_sample: int = end_of_sustain_sample + round(self.release_time * sample_rate)

        if 0 <= sample <= end_of_attack_sample:
            phase = sample / end_of_attack_sample
            return self._get_curve_value(0, 1.0, self.attack_curve, phase)
        elif end_of_attack_sample < sample <= end_of_decay_sample:
            phase = (sample - end_of_attack_sample) / (end_of_decay_sample-end_of_attack_sample)
            return self._get_curve_value(1.0, self.sustain_level, self.decay_curve, phase)
        elif end_of_decay_sample < sample <= end_of_sustain_sample:
            return self.sustain_level
        elif end_of_sustain_sample < sample <= end_of_release_sample:
            phase = (sample - end_of_sustain_sample) / (end_of_release_sample - end_of_sustain_sample)
            return self._get_curve_value(self.sustain_level, 0, self.release_curve, phase)
        else:
            return 0.0

    @staticmethod
    def _get_curve_value(start_val: float, end_val: float, curve: float, phase: float):
        return start_val + (end_val - start_val) * phase

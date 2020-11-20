import numpy as np

from py_headless_daw.dsp_utils.curve import get_curve_value
from py_headless_daw.dsp_utils.wave_producer_interface import WaveProducerInterface


# https://en.wikipedia.org/wiki/Envelope_(music)#ADSR
class ADSREnvelope(WaveProducerInterface):

    def __init__(self, attack_time: float, decay_time: float, sustain_level: float, sustain_time: float,
                 release_time: float):
        self.attack_time: float = attack_time
        self.decay_time: float = decay_time
        self.sustain_level: float = sustain_level
        self.sustain_time: float = sustain_time
        self.release_time: float = release_time

        self.attack_curve: float = 0  # 0 means linear, other values in [-1, 1] range (will) be different extents of curveness
        self.decay_curve: float = 0
        self.release_curve: float = 0

        self.attack_curve_power: float = 2.0
        self.decay_curve_power: float = 2.0
        self.release_curve_power: float = 3.0

    def render_to_buffer(self, output_buffer: np.ndarray, sample_rate: int, start_sample: int, mode: str = WaveProducerInterface.MODE_REPLACE):
        for i in range(output_buffer.shape[0]):
            output_buffer[i] = self.get_one_value(start_sample + i, sample_rate)

    def get_one_value(self, sample: int, sample_rate: int) -> float:
        end_of_attack_sample: int = round(self.attack_time * sample_rate)
        end_of_decay_sample: int = end_of_attack_sample + round(self.decay_time * sample_rate)
        end_of_sustain_sample: int = end_of_decay_sample + round(self.sustain_time * sample_rate)
        end_of_release_sample: int = end_of_sustain_sample + round(self.release_time * sample_rate)

        if 0 <= sample <= end_of_attack_sample:
            if end_of_attack_sample == 0:
                return 1.0

            phase = sample / end_of_attack_sample
            return get_curve_value(0, 1.0, self.attack_curve, self.attack_curve_power, phase)
        elif end_of_attack_sample < sample <= end_of_decay_sample:
            if sample == end_of_decay_sample:
                return self.sustain_level
            phase = (sample - end_of_attack_sample) / (end_of_decay_sample - end_of_attack_sample)
            return get_curve_value(1.0, self.sustain_level, self.decay_curve, self.decay_curve_power, phase)
        elif end_of_decay_sample < sample <= end_of_sustain_sample:
            if sample == end_of_sustain_sample:
                return self.sustain_level
            return self.sustain_level
        elif end_of_sustain_sample < sample <= end_of_release_sample:
            if sample == end_of_release_sample:
                return 0.0

            phase = (sample - end_of_sustain_sample) / (end_of_release_sample - end_of_sustain_sample)
            return get_curve_value(self.sustain_level, 0, self.release_curve, self.release_curve_power, phase)
        else:
            return 0.0

    @staticmethod
    def _get_curve_value(start_val: float, end_val: float, curve_ratio: float, curve_power: float, phase: float):
        linear_value = start_val + (end_val - start_val) * phase
        if curve_ratio >= 0:
            curve_value = start_val + (end_val - start_val) * (phase ** curve_power)
        else:
            curve_value = start_val + (end_val - start_val) * (1 - (1 - phase) ** curve_power)

        abs_ratio = abs(curve_ratio)

        return linear_value * (1 - abs_ratio) + curve_value * abs_ratio

    def get_length_seconds(self) -> float:
        return self.attack_time + self.decay_time + self.sustain_time + self.release_time

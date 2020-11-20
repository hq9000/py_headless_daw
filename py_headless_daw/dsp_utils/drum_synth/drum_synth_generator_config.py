from dataclasses import dataclass
from typing import List

from py_headless_daw.dsp_utils.wave_types import WAVE_TYPE_SINE


@dataclass
class OscillatorConfig:
    volume: float = 1
    zero_frequency: float = 440
    frequency_range: float = 1000
    start_phase: float = 0
    wave_type: str = WAVE_TYPE_SINE

    volume_envelope_attack_time: float = 0.01
    volume_envelope_attack_curve_ratio: float = 0
    volume_envelope_attack_curve_power: float = 1

    volume_envelope_decay_time: float = 0.3
    volume_envelope_decay_curve_ratio: float = 1
    volume_envelope_decay_curve_power: float = 2

    volume_envelope_sustain_level: float = 0
    volume_envelope_sustain_time: float = 0

    volume_envelope_release_time: float = 1
    volume_envelope_release_curve_ratio: float = 0
    volume_envelope_release_curve_power: float = 2

    pitch_envelope_attack_time: float = 0.01
    pitch_envelope_attack_curve_ratio: float = 0
    pitch_envelope_attack_curve_power: float = 2

    pitch_envelope_decay_time: float = 0.4
    pitch_envelope_decay_curve_ratio: float = 0.5
    pitch_envelope_decay_curve_power: float = 2

    pitch_envelope_sustain_level: float = 0
    pitch_envelope_sustain_time: float = 0
    pitch_envelope_release_time: float = 1
    pitch_envelope_release_curve_ratio: float = 1
    pitch_envelope_release_curve_power: float = 2


class DrumSynthGeneratorConfig:
    def __init__(self, oscillators_configs: List[OscillatorConfig]):
        self.oscillator_configs = oscillators_configs

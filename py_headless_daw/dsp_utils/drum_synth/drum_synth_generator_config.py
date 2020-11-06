from dataclasses import dataclass
from typing import List


@dataclass
class OscillatorConfig:
    volume: float
    frequency: float
    start_phase: float
    wave_type: str =

    volume_envelope_attack_time: float
    volume_envelope_attack_curve_ratio: float
    volume_envelope_attack_curve_power: float

    volume_envelope_decay_time: float
    volume_envelope_decay_curve_ratio: float
    volume_envelope_decay_curve_power: float

    volume_envelope_sustain_level: float
    volume_envelope_sustain_time: float

    volume_envelope_release_time: float
    volume_envelope_release_curve_ratio: float
    volume_envelope_release_curve_power: float

    pitch_envelope_attack_time: float
    pitch_envelope_attack_curve_ratio: float
    pitch_envelope_attack_curve_power: float

    pitch_envelope_decay_time: float
    pitch_envelope_decay_curve: float
    pitch_envelope_decay_curve_power: float

    pitch_envelope_sustain_level: float
    pitch_envelope_sustain_time: float

    pitch_envelope_release_time: float
    pitch_envelope_release_curve: float
    pitch_envelope_release_curve_power: float


class DrumSynthGeneratorConfig:
    def __init__(self, oscillators_configs: List[OscillatorConfig]):
        self.oscillator_configs = oscillators_configs

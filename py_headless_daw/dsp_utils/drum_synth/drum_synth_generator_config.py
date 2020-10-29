from dataclasses import dataclass
from typing import List


@dataclass
class OscillatorConfig:
    volume: float

    volume_envelope_attack: float
    volume_envelope_decay: float
    volume_envelope_sustain: float
    volume_envelope_release: float

    pitch: float

    pitch_envelope_attack: float
    pitch_envelope_decay: float
    pitch_envelope_sustain: float
    pitch_envelope_release: float

    frequency: float


class DrumSynthGeneratorConfig:
    def __init__(self, oscillators_configs: List[OscillatorConfig]):
        self.oscillator_configs = oscillators_configs

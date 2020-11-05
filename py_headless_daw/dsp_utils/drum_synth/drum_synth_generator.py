from typing import List

import numpy as np

from py_headless_daw.dsp_utils.adsr_envelope import ADSREnvelope
from py_headless_daw.dsp_utils.drum_synth.drum_synth_generator_config import DrumSynthGeneratorConfig
from py_headless_daw.dsp_utils.drum_synth.one_shot_oscillator import OneShotOscillator
from py_headless_daw.dsp_utils.wave_producer_interface import WaveProducerInterface


class DrumSynthGenerator(WaveProducerInterface):

    def __init__(self, config: DrumSynthGeneratorConfig):
        self._oscillators: List[OneShotOscillator] = []
        for oscillator_config in config.oscillator_configs:
            new_osc = OneShotOscillator()
            volume_envelope = ADSREnvelope(oscillator_config.volume_envelope_attack,
                                           oscillator_config.volume_envelope_decay,
                                           oscillator_config.volume_envelope_sustain,
                                           oscillator_config.volume_envelope_release)

            pitch_envelope = ADSREnvelope(oscillator_config.pitch_envelope_attack,
                                          oscillator_config.pitch_envelope_decay,
                                          oscillator_config.pitch_envelope_sustain,
                                          oscillator_config.pitch_envelope_release)

            new_osc.pitch_envelope = pitch_envelope
            new_osc.volume_envelope = volume_envelope

            new_osc.frequency = oscillator_config.frequency
            new_osc.volume = oscillator_config.volume

    def render_to_buffer(self, output_buffer: np.ndarray, sample_rate: int, start_sample: int):
        pass

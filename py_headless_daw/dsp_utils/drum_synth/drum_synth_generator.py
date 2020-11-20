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
            volume_envelope = ADSREnvelope(oscillator_config.volume_envelope_attack_time,
                                           oscillator_config.volume_envelope_decay_time,
                                           oscillator_config.volume_envelope_sustain_level,
                                           oscillator_config.volume_envelope_sustain_time,
                                           oscillator_config.volume_envelope_release_time)

            volume_envelope.attack_curve_power = oscillator_config.volume_envelope_attack_curve_power
            volume_envelope.attack_curve = oscillator_config.volume_envelope_attack_curve_ratio

            volume_envelope.decay_curve_power = oscillator_config.volume_envelope_decay_curve_power
            volume_envelope.decay_curve = oscillator_config.volume_envelope_decay_curve_ratio

            volume_envelope.release_curve_power = oscillator_config.volume_envelope_release_curve_power
            volume_envelope.release_curve = oscillator_config.volume_envelope_release_curve_ratio

            pitch_envelope = ADSREnvelope(oscillator_config.pitch_envelope_attack_time,
                                          oscillator_config.pitch_envelope_decay_time,
                                          oscillator_config.pitch_envelope_sustain_level,
                                          oscillator_config.pitch_envelope_sustain_time,
                                          oscillator_config.pitch_envelope_release_time)

            pitch_envelope.attack_curve_power = oscillator_config.volume_envelope_attack_curve_power
            pitch_envelope.attack_curve = oscillator_config.volume_envelope_attack_curve_ratio

            pitch_envelope.decay_curve_power = oscillator_config.pitch_envelope_decay_curve_power
            pitch_envelope.decay_curve = oscillator_config.pitch_envelope_decay_curve_ratio

            pitch_envelope.release_curve_power = oscillator_config.pitch_envelope_release_curve_power
            pitch_envelope.release_curve = oscillator_config.pitch_envelope_release_curve_ratio

            new_osc.pitch_envelope = pitch_envelope
            new_osc.volume_envelope = volume_envelope

            new_osc.zero_frequency = oscillator_config.zero_frequency
            new_osc.frequency_range = oscillator_config.frequency_range

            new_osc.volume = oscillator_config.volume

            new_osc.initial_phase = oscillator_config.start_phase

            self._oscillators.append(new_osc)

    def render_to_buffer(self, output_buffer: np.ndarray, sample_rate: int, start_sample: int,
                         mode: str = WaveProducerInterface.MODE_REPLACE):

        for pos, oscillator in enumerate(self._oscillators):

            if pos == 0:
                mode = WaveProducerInterface.MODE_REPLACE
            else:
                mode = WaveProducerInterface.MODE_MIX

            oscillator.render_to_buffer(output_buffer, sample_rate, start_sample, mode)

    def get_length_of_full_hit_seconds(self) -> float:
        """
        tells how many samples are needed to fully render a hit with current settings

        It does it by examining volume envelopes of all of the oscillators and
        returning the maximum length of them.
        """
        max_length: float = 0.0
        for osc in self._oscillators:
            current_max = osc.volume_envelope.get_length_seconds()
            if current_max > max_length:
                max_length = current_max

        return max_length

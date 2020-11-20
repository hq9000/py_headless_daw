import unittest
from copy import copy

import numpy as np

from py_headless_daw.dsp_utils.drum_synth.drum_synth_generator import DrumSynthGenerator
from py_headless_daw.dsp_utils.drum_synth.drum_synth_generator_config import DrumSynthGeneratorConfig, OscillatorConfig
from py_headless_daw.dsp_utils.wave_types import WAVE_TYPE_SINE


# import matplotlib.pyplot as plt


class MyTestCase(unittest.TestCase):
    def test_generate_bd_with_two_oscillators(self):
        osc_config1 = OscillatorConfig(
            wave_type=WAVE_TYPE_SINE,
            volume=1,
            zero_frequency=0,
            frequency_range=300,
            start_phase=0,

            volume_envelope_attack_time=0.001,

            volume_envelope_decay_time=0.1,
            volume_envelope_decay_curve_power=4,
            volume_envelope_decay_curve_ratio=-1,

            volume_envelope_sustain_level=0,

            pitch_envelope_attack_time=0,
            pitch_envelope_decay_time=0.1,
            pitch_envelope_decay_curve_ratio=-0.9,
            pitch_envelope_decay_curve_power=4,
            pitch_envelope_sustain_level=0
        )

        osc_config2 = copy(osc_config1)
        osc_config2.start_phase = 2.123
        osc_config2.frequency_range = 200

        config = DrumSynthGeneratorConfig([osc_config1, osc_config2])
        generator = DrumSynthGenerator(config)

        output_buffer_size = 5000
        output_buffer = np.ndarray(shape=(output_buffer_size,), dtype=np.float32)

        generator.render_to_buffer(output_buffer, 44100, 0)

        # plt.plot(output_buffer)
        # plt.show()


if __name__ == '__main__':
    unittest.main()

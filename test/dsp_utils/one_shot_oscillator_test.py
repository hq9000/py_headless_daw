import unittest

import numpy as np

from py_headless_daw.dsp_utils.adsr_envelope import ADSREnvelope
from py_headless_daw.dsp_utils.drum_synth.one_shot_oscillator import OneShotOscillator


# noinspection PyUnresolvedReferences
# import matplotlib.pyplot as plt


class OneShotOscillatorTestCase(unittest.TestCase):
    def test_get_value(self):
        envelope = ADSREnvelope(
            attack_time=0.1,
            decay_time=0.4,
            sustain_level=0.5,
            sustain_time=0.25,
            release_time=0.25
        )

        osc = OneShotOscillator()

        osc.pitch_envelope = envelope
        osc.volume_envelope = envelope

        output_buffer_size = 1000
        sample_rate = 44100

        output_buffer = np.ndarray(shape=(output_buffer_size,), dtype=np.float32)
        osc.render_to_buffer(output_buffer, sample_rate, 0)

        # plt.plot(output_buffer)
        # plt.show()


if __name__ == '__main__':
    unittest.main()

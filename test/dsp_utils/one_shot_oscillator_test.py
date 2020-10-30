import unittest

import numpy as np

from py_headless_daw.dsp_utils.adsr_envelope import ADSREnvelope
from py_headless_daw.dsp_utils.drum_synth.one_shot_oscillator import OneShotOscillator


class OneShotOscillatorTestCase(unittest.TestCase):
    def test_get_value(self):
        envelope = ADSREnvelope(1, 1, 1, 1)

        osc = OneShotOscillator()

        osc.pitch_envelope = envelope
        osc.volume_envelope = envelope

        output_buffer = np.ndarray(shape=(100,), dtype=np.float32)
        osc.produce(output_buffer, 100, 0)


if __name__ == '__main__':
    unittest.main()

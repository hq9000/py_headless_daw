import unittest

import numpy as np

from py_headless_daw.dsp_utils.adsr_envelope import ADSREnvelope


class ADSREnvelopeTestCase(unittest.TestCase):
    def test_get_value(self):
        envelope = ADSREnvelope(
            attack_time=1,
            decay_time=1,
            sustain_level=0.5,
            sustain_time=1,
            release_time=1
        )

        self.assertEqual(0, envelope.get_value(-1, 1000))
        self.assertEqual(0, envelope.get_value(0, 1000))
        self.assertEqual(0.5, envelope.get_value(500, 1000))
        self.assertEqual(1, envelope.get_value(1000, 1000))
        self.assertEqual(0.75, envelope.get_value(1500, 1000))
        self.assertEqual(0.5, envelope.get_value(2000, 1000))
        self.assertEqual(0.5, envelope.get_value(2500, 1000))
        self.assertEqual(0.5, envelope.get_value(3000, 1000))
        self.assertEqual(0.25, envelope.get_value(3500, 1000))
        self.assertEqual(0.0, envelope.get_value(4000, 1000))
        self.assertEqual(0.0, envelope.get_value(4001, 1000))

    def test_generate_wave(self):
        envelope = ADSREnvelope(
            attack_time=1,
            decay_time=1,
            sustain_level=0.5,
            sustain_time=1,
            release_time=1
        )

        buffer = np.ndarray(shape=(400,), dtype=np.float32)
        envelope.produce(buffer, 100, 0)


if __name__ == '__main__':
    unittest.main()

import unittest

from py_headless_daw.dsp_utils.adsr_envelope import ADSREnvelope


class ADSREnvelopeTestCase(unittest.TestCase):
    def test_get_value(self):
        envelope = ADSREnvelope(1, 1, 1, 1)
        self.assertEqual(1, envelope.get_value(50, 1000))


if __name__ == '__main__':
    unittest.main()

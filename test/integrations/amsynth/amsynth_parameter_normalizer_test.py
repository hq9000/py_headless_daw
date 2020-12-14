import unittest

from py_headless_daw.integrations.amsynth.amsynth_parameter_normalizer import AmsynthParameterNormalizer


class MyTestCase(unittest.TestCase):
    def test_denormalize(self):
        normalizer = AmsynthParameterNormalizer()
        denormalized_val = normalizer.denormalize('amp_attack', 0.059)
        self.assertEqual(0.1475, denormalized_val)

    def test_normalize(self):
        normalizer = AmsynthParameterNormalizer()
        normalized_val = normalizer.normalize('amp_attack', 0.1475)
        self.assertEqual(0.059, normalized_val)


if __name__ == '__main__':
    unittest.main()

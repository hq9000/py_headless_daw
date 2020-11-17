import unittest

import parametrized

from py_headless_daw.dsp_utils.curve import get_curve_value


@parametrized.parametrized_test_case
class MyTestCase(unittest.TestCase):

    @parametrized.parametrized([
        [0.0, 1.0, 0, 2.0, 0, 0],
        [0.0, 1.0, 0, 2.0, 1, 1],

        [0.0, 1.0, 0.5, 2.0, 0.0, 0],
        [0.0, 1.0, 0.5, 2.0, 1.0, 1],
        [0.0, 1.0, 0.5, 2.0, 0.5, 0.375],  # 0.5 / 2 + 0.5 * 0.5 / 2

        [0.0, 1.0, -0.5, 2.0, 0.0, 0],
        [0.0, 1.0, -0.5, 2.0, 1.0, 1],
        [0.0, 1.0, -0.5, 2.0, 0.5, 0.625]
    ])
    def one_value(self, start_val: float, end_val: float, curve_ratio: float,
                  curve_power: float, phase: float,
                  expected_value: float):
        self.assertEquals(expected_value, get_curve_value(
            start_val=start_val,
            end_val=end_val,
            curve_ratio=curve_ratio,
            curve_power=curve_power,
            phase=phase))


if __name__ == '__main__':
    unittest.main()

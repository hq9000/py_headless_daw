import unittest

import parametrized as parametrized


@parametrized.parametrized_test_case
class MyTestCase(unittest.TestCase):

    @parametrized.parametrized([
        (1, 2, 3, 4, 5, 6, 7, 8)
    ])
    def test_get_intersection_with_interval(self,
                                            interval_start: float,
                                            interval_end: float,
                                            clip_start: float,
                                            clip_end: float,
                                            intersection_start: float,
                                            intersection_end: float,
                                            intersection_start_clip_time: float,
                                            intersection_end_clip_time_float):
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()

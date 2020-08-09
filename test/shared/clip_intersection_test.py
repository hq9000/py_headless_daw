import unittest

import parametrized as parametrized

from py_headless_daw.project.content.clip import Clip
from py_headless_daw.schema.dto.time_interval import TimeInterval
from py_headless_daw.shared.clip_intersection import ClipIntersection


@parametrized.parametrized_test_case
class ClipIntersectionTest(unittest.TestCase):

    @parametrized.parametrized([
        (1, 4, 2, 3, 2, 3, 0, 1),
        (1, 2, 3, 4, None),
        (3, 4, 1, 2, None),
        (1, 3, 2, 4, 2, 3, 0, 1)
    ])
    def get_intersection_with_interval(self,
                                       interval_start: float,
                                       interval_end: float,
                                       clip_start: float,
                                       clip_end: float,
                                       expected_intersection_start: float = None,
                                       expected_intersection_end: float = None,
                                       expected_intersection_start_clip_time: float = None,
                                       expected_intersection_end_clip_time: float = None):
        interval = TimeInterval()
        interval.start_in_seconds = interval_start
        interval.end_in_seconds = interval_end

        clip = Clip(clip_start, clip_end)

        intersection = ClipIntersection.create_intersection_of_clip_and_interval(clip, interval)

        if expected_intersection_start is None:
            self.assertIsNone(intersection)
            return

        self.assertEqual(expected_intersection_start, intersection.start_project_time,
                         "unexpected intersection start project time")
        self.assertEqual(expected_intersection_end, intersection.end_project_time,
                         "unexpected intersection end project time")
        self.assertEqual(expected_intersection_start_clip_time, intersection.start_clip_time,
                         "unexpected intersection start clip time")
        self.assertEqual(expected_intersection_end_clip_time, intersection.end_clip_time,
                         "unexpected intersection end clip time")

        self.assertIs(clip, intersection.clip)


if __name__ == '__main__':
    unittest.main()

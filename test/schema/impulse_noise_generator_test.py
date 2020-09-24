import unittest

import numpy as np

from py_headless_daw.processing.stream.impulse_noice_generator import ImpulseNoiseGeneratorStrategy
from py_headless_daw.schema.dto.time_interval import TimeInterval


class ImpulseNoiseGeneratorStrategyTest(unittest.TestCase):

    @staticmethod
    def test_impulse_noise_generator_strategy():
        strategy = ImpulseNoiseGeneratorStrategy()
        out_stream_buffer = np.zeros(shape=(100,), dtype=np.float32)

        interval = TimeInterval()
        interval.start_in_bars = 0
        interval.end_in_bars = 1

        strategy.render(interval, [], [out_stream_buffer], [], [])

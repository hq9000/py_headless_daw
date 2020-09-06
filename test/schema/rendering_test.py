import unittest

import numpy as np

from py_headless_daw.processing.hybrid.transparent_strategy import Transparent
from py_headless_daw.processing.stream.constant_level import ConstantLevel
from py_headless_daw.processing.stream.stream_gain import StreamGain
from py_headless_daw.schema.dto.time_interval import TimeInterval
from py_headless_daw.schema.host import Host
from py_headless_daw.schema.unit import Unit
from py_headless_daw.schema.wiring import Connector


class RenderingTest(unittest.TestCase):
    def test_fork_and_join(self):
        # +--------+     +--------+
        # |        |     |        |
        # | level1 +--+--> gain1  +--+
        # |        |  |  |        |  | +--------+
        # +--------+  |  +--------+  | |        |
        #             |              +-> mixer  |
        #             |              | |        |
        # +--------+  |  +--------+  | +--------+
        # |        +--+  |        |  |
        # | level2 +-----> gain2  +--+
        # |        |     |        |
        # +--------+     +--------+
        gain1_value = np.float32(0.7)
        gain2_value = np.float32(0.113)

        level1_value = np.float32(0.63)
        level2_value = np.float32(0.47)

        host = Host()

        level1 = Unit(0, 0, 1, 0, host, ConstantLevel(level1_value))
        level2 = Unit(0, 0, 1, 0, host, ConstantLevel(level2_value))

        gain1 = Unit(1, 0, 1, 0, host, StreamGain(gain1_value))
        gain2 = Unit(1, 0, 1, 0, host, StreamGain(gain2_value))

        mixer = Unit(1, 0, 1, 0, host, Transparent())

        Connector(level1.output_stream_nodes[0], gain1.input_stream_nodes[0])
        Connector(level2.output_stream_nodes[0], gain2.input_stream_nodes[0])
        Connector(level2.output_stream_nodes[0], gain1.input_stream_nodes[0])

        Connector(gain1.output_stream_nodes[0], mixer.input_stream_nodes[0])
        Connector(gain2.output_stream_nodes[0], mixer.input_stream_nodes[0])

        interval = TimeInterval()
        interval.start_in_bars = 0
        interval.end_in_bars = 1
        interval.start_in_seconds = -0.1
        interval.end_in_seconds = 0.333333333
        interval.num_samples = 44100 * interval.get_length_in_seconds()

        out_buffer = np.ndarray(shape=(100,), dtype=np.float32)
        mixer.output_stream_nodes[0].render(interval, out_buffer)

        expected_output_level = (level1_value + level2_value) * gain1_value + level2_value * gain2_value

        for x in range(0, 100):
            self.assertEqual(expected_output_level, out_buffer[x])

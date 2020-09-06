import unittest

import numpy as np

from py_headless_daw.processing.stream.constant_level import ConstantLevel
from py_headless_daw.processing.stream.stream_gain import StreamGain
from py_headless_daw.schema.chain import Chain
from py_headless_daw.schema.dto.time_interval import TimeInterval
from py_headless_daw.schema.host import Host
from py_headless_daw.schema.unit import Unit
from py_headless_daw.schema.wiring import Connector


class ChainTest(unittest.TestCase):
    def test_chaining_two_stream_units(self):
        host = Host()
        unit1 = Unit(0, 0, 1, 0, host, ConstantLevel(np.float32(0.5)))
        unit2 = Unit(1, 0, 1, 0, host, StreamGain(np.float32(0.5)))
        Connector(unit1.output_stream_nodes[0], unit2.input_stream_nodes[0])

        chain = Chain(unit1, unit2)

        self.assertEqual(len(chain.input_stream_nodes), 0)
        self.assertEqual(len(chain.input_event_nodes), 0)
        self.assertEqual(len(chain.output_stream_nodes), 1)
        self.assertEqual(len(chain.output_event_nodes), 0)

        interval = TimeInterval()
        interval.start_in_bars = 0
        interval.end_in_bars = 1

        interval.start_in_seconds = 0.0
        interval.end_in_seconds = 0.25

        interval.num_samples = 44100 * interval.get_length_in_seconds()
        out_buffer = np.ndarray(shape=(100,), dtype=np.float32)
        chain.output_stream_nodes[0].render(interval, out_buffer)

        for x in range(0, 100):
            self.assertEqual(0.25, out_buffer[x])

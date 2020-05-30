import unittest
from typing import List

import numpy as np

from py_headless_daw.processing.stream.stream_gain import StreamGain
from py_headless_daw.schema.dto.time_interval import TimeInterval
from py_headless_daw.schema.events.event import Event
from py_headless_daw.schema.events.parameter_value_event import ParameterValueEvent


class StreamGainStrategyTest(unittest.TestCase):

    def test_stream_gain_strategy(self):
        strategy = StreamGain(np.float32(0.25))

        interval = TimeInterval()
        interval.start_in_bars = 0
        interval.end_in_bars = 1

        in_stream_buffer = np.ones(shape=(100,), dtype=np.float32)
        out_stream_buffer = np.zeros(shape=(100,), dtype=np.float32)

        setter_event: ParameterValueEvent = ParameterValueEvent(0, StreamGain.PARAMETER_GAIN, 0.55)

        input_event_buffer: List[Event] = [setter_event]
        output_event_buffer: List[Event] = []

        strategy.render(interval, [in_stream_buffer], [out_stream_buffer], [input_event_buffer], [output_event_buffer])

        for x in range(0, 100):
            self.assertTrue(0.54 < out_stream_buffer[x] < 0.56)

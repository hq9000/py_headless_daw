import unittest

import numpy as np

from py_headless_daw.processing.hybrid.drum_synth_strategy import DrumSynthStrategy
from py_headless_daw.project.plugins.drum_synth_plugin import DrumSynthPlugin
from py_headless_daw.schema.dto.time_interval import TimeInterval
from py_headless_daw.schema.events.midi_event_factory import MidiEventFactory
from py_headless_daw.schema.host import Host
from py_headless_daw.schema.unit import Unit
# import matplotlib.pyplot as plt


class DrumSynthStrategyTestCase(unittest.TestCase):
    def test_render_one_buffer_with_a_note(self):
        plugin = DrumSynthPlugin()

        host = Host()
        strategy = DrumSynthStrategy(plugin)
        Unit(0, 0, 1, 0, host, strategy)

        out_stream_buffer = np.zeros(shape=(100,), dtype=np.float32)

        interval = TimeInterval()
        interval.start_in_bars = 0
        interval.end_in_bars = 1

        factory = MidiEventFactory()

        note_event = factory.create_note_on_event(note=65, velocity=70, position=50)

        strategy.render(interval, [], [out_stream_buffer], [[note_event]], [])

        zero_sample_indices = [0, 20, 40]
        non_zero_sample_indices = [60, 80, 99]

        for idx in zero_sample_indices:
            self.assertEqual(0, out_stream_buffer[idx])

        for idx in non_zero_sample_indices:
            self.assertNotEqual(0, out_stream_buffer[idx])


if __name__ == '__main__':
    unittest.main()

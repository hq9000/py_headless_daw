import os
import unittest
from typing import List

import numpy as np

from py_headless_daw.processing.hybrid.vst_plugin import VstPlugin
from py_headless_daw.schema.dto.time_interval import TimeInterval
from py_headless_daw.schema.events.event import Event
from py_headless_daw.schema.events.midi_event_factory import MidiEventFactory
from py_headless_daw.schema.host import Host
from py_headless_daw.schema.unit import Unit


class VstPluginProcessingStrategyTest(unittest.TestCase):

    def test_vst_plugin_strategy(self):
        host = Host()

        dir_path = os.path.dirname(os.path.realpath(__file__))

        path_to_so: str = dir_path + '/../test_plugins/amsynth-vst.x86_64-linux.so'
        as_bytes = path_to_so.encode('utf-8')

        unit = Unit(0, 0, 1, 0, host)
        strategy = VstPlugin(as_bytes, unit)

        unit.set_processing_strategy(strategy)
        event_factory = MidiEventFactory()
        event = event_factory.create_note_on_event(87, 10)
        event.sample_position = 9
        events: List[Event] = [event]

        def generate():
            return np.zeros((host.block_size,), np.float32)

        left_out = generate()
        right_out = generate()

        interval = TimeInterval()
        interval.start_in_bars = 0
        interval.end_in_bars = 1
        interval.num_samples = 100

        self.assertTrue(left_out[13] == 0.0)
        self.assertTrue(right_out[13] == 0.0)

        strategy.render(interval, [], [left_out, right_out], [events], [])

        self.assertTrue(left_out[13] != 0.0)
        self.assertTrue(right_out[13] != 0.0)

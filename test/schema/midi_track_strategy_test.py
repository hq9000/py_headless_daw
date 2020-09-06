import unittest
from typing import cast

from py_headless_daw.processing.event.midi_track_strategy import MidiTrackStrategy
from py_headless_daw.project.content.midi_clip import MidiClip
from py_headless_daw.project.content.midi_note import MidiNote
from py_headless_daw.project.midi_track import MidiTrack
from py_headless_daw.schema.dto.time_interval import TimeInterval
from py_headless_daw.schema.events.midi_event import MidiEvent


class MidiTrackStrategyTest(unittest.TestCase):
    def test_something(self):
        track = self._generate_midi_track()
        strategy = MidiTrackStrategy(track)

        outputs = [[]]

        interval = TimeInterval()
        interval.start_in_seconds = 0.0
        interval.end_in_seconds = 1.0
        interval.start_in_bars = 0.0
        interval.end_in_bars = 1.0
        interval.num_samples = 100

        strategy.render(interval, [], [], [], outputs)

        output = outputs[0]

        self.assertEqual(2, len(output))  # note on and note off

        first_event: MidiEvent = cast(MidiEvent, output[0])
        second_event: MidiEvent = cast(MidiEvent, output[1])

        self.assertIsInstance(first_event, MidiEvent)
        self.assertIsInstance(second_event, MidiEvent)

        self.assertEqual(0, first_event.sample_position)
        self.assertEqual(10, second_event.sample_position)

    @staticmethod
    def _generate_midi_track() -> MidiTrack:
        track = MidiTrack(1)
        clip = MidiClip(0.0, 1.0)
        clip.midi_notes = [
            MidiNote(clip, 0.0, 65, 65, 0.1)
        ]
        track.clips = [
            clip
        ]
        return track

from typing import List, cast

import numpy as np

from py_headless_daw.project.content.midi_clip import MidiClipEvent
from py_headless_daw.project.content.midi_note import MidiNote
from py_headless_daw.project.midi_track import MidiTrack
from py_headless_daw.schema.dto.time_interval import TimeInterval
from py_headless_daw.schema.events.event import Event
from py_headless_daw.schema.events.midi_event import MidiEvent
from py_headless_daw.schema.events.midi_event_factory import MidiEventFactory
from py_headless_daw.schema.processing_strategy import ProcessingStrategy


class MidiTrackStrategy(ProcessingStrategy):
    def __init__(self, track: MidiTrack):
        super().__init__()
        self.track = track
        self._midi_event_factory: MidiEventFactory = MidiEventFactory()

    def render(self, interval: TimeInterval, stream_inputs: List[np.ndarray], stream_outputs: List[np.ndarray],
               event_inputs: List[List[Event]], event_outputs: List[List[Event]]):

        clip_events: List[MidiClipEvent] = self.track.get_events(interval.start_in_seconds, interval.end_in_seconds)
        midi_event_lists: List[List[MidiEvent]] = []
        for event in clip_events:
            midi_event_lists.append(self._clip_event_transformer(interval, event))

        for event_output in event_outputs:
            for midi_event_list in midi_event_lists:
                for midi_event in midi_event_list:
                    event_output.append(midi_event)

    @staticmethod
    def round(a: float) -> float:
        return round(a, 5)

    def _clip_event_transformer(self, interval: TimeInterval, clip_event: MidiClipEvent) -> List[MidiEvent]:
        """
        the result can be multiple events

        :param interval:
        :param clip_event:
        :return:
        """
        if isinstance(clip_event, MidiNote):
            midi_note: MidiNote = cast(MidiNote, clip_event)
            return self._convert_midi_note_to_events(interval, midi_note)
        else:
            return []

    def _convert_midi_note_to_events(self, interval: TimeInterval, midi_note: MidiNote) -> List[MidiEvent]:
        note_start_in_seconds = midi_note.get_absolute_start_time()
        note_end_in_seconds = midi_note.get_absolute_end_time()

        if note_start_in_seconds > interval.end_in_seconds:
            raise Exception(
                'note start falls to the right of the interval: ' + str(note_start_in_seconds) + ' > ' + str(
                    interval.end_in_seconds) + '. It should not have happened, must be a bug')

        if note_end_in_seconds < interval.start_in_seconds:
            raise Exception('note ends falls to the left of the interval: ' + str(note_end_in_seconds) + ' < ' + str(
                interval.start_in_seconds) + '. It should not have happened, must be a bug')

        res: List[MidiEvent] = []

        if self.round(note_start_in_seconds) >= self.round(interval.start_in_seconds):
            sample_position = self._calculate_sample_position(interval, self.round(note_start_in_seconds))
            res.append(
                self._midi_event_factory.create_note_on_event(midi_note.note, midi_note.velocity, sample_position))

        if self.round(note_end_in_seconds) <= self.round(interval.end_in_seconds):
            sample_position = self._calculate_sample_position(interval, self.round(note_end_in_seconds))
            if sample_position == interval.num_samples:
                sample_position -= 1

            res.append(
                self._midi_event_factory.create_note_off_event(midi_note.note, midi_note.velocity, sample_position))

        return res

    @staticmethod
    def _calculate_sample_position(interval: TimeInterval, event_time_in_seconds: float) -> int:

        tolerance: float = 0.00000000001

        assert interval.start_in_seconds - tolerance <= event_time_in_seconds < interval.end_in_seconds + tolerance, \
            'event time %5.5f is out of interval [%5.5f, %5.5f)' % (
                event_time_in_seconds, interval.start_in_seconds, interval.end_in_seconds
            )

        relative_time_in_seconds = event_time_in_seconds - interval.start_in_seconds
        assert 0 - tolerance <= relative_time_in_seconds < interval.get_length_in_seconds() + tolerance

        return round(interval.num_samples * relative_time_in_seconds / interval.get_length_in_seconds())

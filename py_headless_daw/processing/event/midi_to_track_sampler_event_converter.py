from typing import List

import numpy as np

from em.platform.rendering.dto.time_interval import TimeInterval
from em.platform.rendering.schema.events.event import Event
from em.platform.rendering.schema.events.midi_event import MidiEvent
from em.platform.rendering.schema.events.track_sampler_event import TrackSamplerEvent
from em.platform.rendering.schema.processing_strategy import ProcessingStrategy


class MidiToTrackSamplerEventConverter(ProcessingStrategy):

    def __init__(self, sample_file_name: str, start_sample: int, end_sample: int = -1):
        self.sample_file_name: str = sample_file_name
        self.start_sample: int = start_sample
        self.end_sample: int = end_sample

    def render(self, interval: TimeInterval, stream_inputs: List[np.ndarray], stream_outputs: List[np.ndarray],
               event_inputs: List[List[Event]], event_outputs: List[List[Event]]):

        for i in range(0, len(event_inputs)):
            for event in event_inputs[i]:
                if event.get_event_type() == Event.TYPE_MIDI:
                    midi_event: MidiEvent = event
                    event_outputs[i].append(self._get_converted(midi_event))

    def _get_converted(self, event: MidiEvent) -> TrackSamplerEvent:
        res = TrackSamplerEvent(event.sample_position)

        res.sample_file_name = self.sample_file_name
        res.sample_start_sample = self.start_sample
        res.sample_end_sample = self.end_sample

        if event.is_note_on():
            res.sample_gain = event.get_velocity() / 128
        if event.is_note_off():
            res.sample_is_off = True

        return res

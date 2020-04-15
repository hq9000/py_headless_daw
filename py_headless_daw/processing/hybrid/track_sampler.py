import copy
from typing import List

import numpy as np

from em.platform.rendering.dto.time_interval import TimeInterval
from em.platform.rendering.sample_management.sample_manager import SampleManager
from em.platform.rendering.schema.events.event import Event
from em.platform.rendering.schema.events.track_sampler_event import TrackSamplerEvent
from em.platform.rendering.schema.processing_strategy import ProcessingStrategy


class TrackSampler(ProcessingStrategy):

    def __init__(self, sample_manager: SampleManager):
        self._left_over_event: TrackSamplerEvent = self._construct_off_event(0)
        self.sample_manager: SampleManager = sample_manager

    def render(self, interval: TimeInterval, stream_inputs: List[np.ndarray], stream_outputs: List[np.ndarray],
               event_inputs: List[List[Event]], event_outputs: List[List[Event]]):
        events = self._filter_events(event_inputs, Event.TYPE_TRACK_SAMPLER)

        # do we have any events from track for sample position 0?
        # if not, we add a "virtual" event at sample 0, we need it to
        # make inner algorithm more generic
        if self._virtual_event_is_needed(events):
            events.append(self._left_over_event)

        events = sorted(events, key=lambda event: event.sample_position)

        buffer_length: int = len(stream_outputs[0])

        for i in range(0, len(events)):
            end_sample: int = buffer_length
            if i < len(events) - 1:
                end_sample = events[i + 1].sample_position

            # noinspection PyTypeChecker
            self._left_over_event = self._process_atomic_region(events[i], events[i].sample_position, end_sample, stream_outputs)

    def _process_atomic_region(self, start_event: TrackSamplerEvent, start_sample: int, end_sample: int,
                               stream_outputs: List[np.ndarray]) -> TrackSamplerEvent:
        if start_event.sample_is_off:
            return self._construct_off_event(0)

        region_length_in_samples: int = end_sample - start_sample

        sample_data: List[np.ndarray] = self.sample_manager.get_sample_data(start_event.sample_file_name,
                                                                            start_event.sample_start_sample,
                                                                            start_event.sample_start_sample +
                                                                            region_length_in_samples)

        self._apply_sample_data_to_buffer(sample_data, stream_outputs, start_sample, start_event)

        sample = self.sample_manager.get_sample(start_event.sample_file_name)
        if sample.get_sample_length() <= start_event.sample_start_sample + region_length_in_samples:
            return self._construct_off_event(0)
        else:
            new_event: TrackSamplerEvent = copy.copy(start_event)
            new_event.sample_start_sample += region_length_in_samples
            new_event.sample_position = 0
            return new_event

    def _construct_off_event(self, position: int) -> TrackSamplerEvent:
        event: TrackSamplerEvent = TrackSamplerEvent(position)
        event.sample_is_off = True
        return event

    def _get_tag_for_sample(self, sample_file_name: str):
        return sample_file_name
        pass

    def _apply_sample_data_to_buffer(self, sample_data: List[np.ndarray], stream_outputs: List[np.ndarray],
                                     start_sample: int, event: TrackSamplerEvent):

        for i in range(0, len(sample_data)):
            self._apply_one_sample_channel_to_buffer(sample_data[i], stream_outputs[i], start_sample, event)

    def _apply_one_sample_channel_to_buffer(self, sample_data: np.ndarray, buffer: np.ndarray, start_sample: int,
                                            event: TrackSamplerEvent):

        length_of_sample_data: int = len(sample_data)  # can be less than buffer
        buffer[start_sample:start_sample + length_of_sample_data] = sample_data
        if event.sample_gain != 1.0:
            buffer[start_sample:start_sample + length_of_sample_data] *= event.sample_gain

    def _virtual_event_is_needed(self, real_events: List[Event]):
        for event in real_events:
            if event.sample_position == 0:
                return False
        return True

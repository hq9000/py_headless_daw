from copy import copy, deepcopy
from dataclasses import dataclass
from math import ceil
from typing import List, Optional, Dict, Union, cast

import numpy as np

from py_headless_daw.dsp_utils.drum_synth.drum_synth_generator import DrumSynthGenerator
from py_headless_daw.project.plugins.drum_synth_plugin import DrumSynthPlugin
from py_headless_daw.schema.dto.time_interval import TimeInterval
from py_headless_daw.schema.events.event import Event
from py_headless_daw.schema.events.midi_event import MidiEvent
from py_headless_daw.schema.events.parameter_value_event import ParameterValueEvent
from py_headless_daw.schema.processing_strategy import ProcessingStrategy

# import matplotlib.pyplot as plt


@dataclass
class Hit:
    data: np.ndarray
    start_sample_in_hit: int
    start_sample_in_buffer: int
    sample_length: int


class DrumSynthStrategy(ProcessingStrategy):

    def __init__(self, plugin: DrumSynthPlugin):

        self._cached_sound: Optional[np.ndarray] = None
        self._unfinished_hits: List[Hit] = []

        # we will use this one as something that holds parameters,
        # tracks parameter changes, and generates generators
        self._plugin: DrumSynthPlugin = deepcopy(plugin)

        super().__init__()

    def render(self, interval: TimeInterval, stream_inputs: List[np.ndarray], stream_outputs: List[np.ndarray],
               event_inputs: List[List[Event]], event_outputs: List[List[Event]]):
        all_events = self._flatten_event_inputs(event_inputs)
        all_events = sorted(all_events, key=lambda event: event.sample_position)

        parameter_value_events = [e for e in all_events if
                                  isinstance(e, ParameterValueEvent)]  # type: List[ParameterValueEvent]

        midi_note_on_events = [e for e in all_events if
                               isinstance(e, MidiEvent) and e.is_note_on()]  # type: List[MidiEvent]

        for event in parameter_value_events:
            # something has changed, so we conservatively
            # invalidate the cache
            #
            # importantly, though, existing hits (i.e. unfinished ones)
            # will still reference the old cache and, therefore, their
            # rendering will be finalized appropriately, after which their
            # remembered cache values will be garbage collected.
            self._invalidate_cache()
            self._plugin.set_parameter_value(event.parameter_id, event.value)

        if self._cached_sound is None:  # the cache was not initialized or has been invalidated
            if self.unit is None:
                raise ValueError('unit is None, which was not expected (error: 0faca3c9)')
            self._regenerate_cache(self.unit.host.sample_rate)

        new_hits = self._convert_note_events_to_new_hits(midi_note_on_events)

        all_hits = [*new_hits, *self._unfinished_hits]

        self._zero_outputs(stream_outputs)

        self._unfinished_hits = self._apply_hits_to_outputs(stream_outputs, all_hits)
        pass

    def _apply_hits_to_outputs(self, stream_outputs: List[np.ndarray], hits: List[Hit]) -> List[Hit]:
        """
        renders all hits to outputs, returns a list hits to be passed to the next iteration

        :param stream_outputs: List of buffers to apply hits to
        :param hits: all hits to apply to current buffers
        :returns: a list of hits to be dealt with on the next iteration
        :rtype: List[Hit]
        """

        hits_for_next_iteration: List[Hit] = []

        for hit in hits:
            hit_for_next: Optional[Hit] = None
            for stream_output in stream_outputs:
                hit_for_next_from_this_channel = self._apply_one_hit_to_one_output(hit, stream_output)
                if hit_for_next is None:
                    # we take the first reported hit for next (presumably from the
                    # first channel)
                    hit_for_next = hit_for_next_from_this_channel

            if hit_for_next is not None:
                hits_for_next_iteration.append(hit_for_next)

        return hits_for_next_iteration

    def _apply_one_hit_to_one_output(self, hit: Hit, stream_output: np.ndarray) -> Optional[Hit]:

        buffer_length = len(stream_output)
        remaining_samples_in_hit = hit.sample_length - hit.start_sample_in_hit
        patch_start_in_output = hit.start_sample_in_buffer
        patch_end_in_output = min(buffer_length, patch_start_in_output + remaining_samples_in_hit)

        patch_length = patch_end_in_output - patch_start_in_output

        patch_start_in_hit = hit.start_sample_in_hit
        patch_end_in_hit = patch_start_in_hit + patch_length

        patched = stream_output[patch_start_in_output:patch_end_in_output]
        patch = hit.data[patch_start_in_hit:patch_end_in_hit]

        np.add(patch, patched, out=patched)

        if patch_end_in_output == buffer_length:
            res = copy(hit)
            res.start_sample_in_hit += patch_length
            res.start_sample_in_buffer = 0
            return res
        else:
            return None

    def _initialize_cache(self):
        # synthesize data to cached_sound
        # detect how long the actual data is until it reliable drops to zero
        self._cached_sound_length_samples = 44100 * 2
        pass

    def _apply_parameter_changes(self, values: Dict[str, Union[str, float]]):
        if len(values):
            self._cached_sound = None

    def _invalidate_cache(self):
        self._cached_sound = None
        self._cached_sound_length_samples = 0

    def _regenerate_cache(self, sample_rate: int):
        generator = DrumSynthGenerator(self._plugin.generate_generator_config())
        needed_length_samples = ceil(generator.get_length_of_full_hit_seconds() * sample_rate)
        self._cached_sound = np.zeros(shape=(needed_length_samples,), dtype=np.float32)
        generator.render_to_buffer(
            output_buffer=self._cached_sound,
            sample_rate=sample_rate,
            start_sample=0)

        # plt.plot(self._cached_sound)
        # plt.show()

    def _convert_note_events_to_new_hits(self, events: List[MidiEvent]) -> List[Hit]:
        res: List[Hit] = []
        cached_sound = cast(np.ndarray, self._cached_sound)
        for event in events:
            hit = Hit(data=self._cached_sound,
                      sample_length=cached_sound.shape[0],
                      start_sample_in_buffer=event.sample_position,
                      start_sample_in_hit=0)
            res.append(hit)

        return res

    def _zero_outputs(self, stream_outputs: List[np.ndarray]):
        for o in stream_outputs:
            o.fill(0)

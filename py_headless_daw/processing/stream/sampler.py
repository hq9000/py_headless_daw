from typing import List, cast, Dict

import numpy as np

from py_headless_daw.dto.waveform import Waveform
from py_headless_daw.project.content.audio_clip import AudioClip
from py_headless_daw.schema.clip_track_processing_strategy import ClipTrackProcessingStrategy
from py_headless_daw.schema.dto.time_interval import TimeInterval
from py_headless_daw.schema.events.event import Event

from py_headless_daw.services.wave_data_provider import WaveformProviderInterface
from py_headless_daw.shared.clip_intersection import ClipIntersection


class ProcessedWavData(Waveform):
    pass


class Sampler(ClipTrackProcessingStrategy):
    """
    Sampler is a strategy that produces audio basing on the number of associated AudioClips
    """

    _processed_wav_data_cache: Dict[str, ProcessedWavData] = {}

    def __init__(self, clips: List[AudioClip], wave_data_provider: WaveformProviderInterface):
        super().__init__(clips)
        for clip in clips:
            if not isinstance(clip, AudioClip):
                raise Exception(f"a clips was expected to be an AudioClip, instead it is {type(clip)}")
        self.clips: List[AudioClip] = clips
        self.wave_data_provider: WaveformProviderInterface = wave_data_provider

    def render(self, interval: TimeInterval, stream_inputs: List[np.ndarray], stream_outputs: List[np.ndarray],
               event_inputs: List[List[Event]], event_outputs: List[List[Event]]):

        if self.unit is None:
            raise Exception('unit is not set in this sampler')

        [o.fill(0.0) for o in stream_outputs]
        intersections = self._find_intersections(interval)

        for intersection in intersections:
            self._render_one_intersection(intersection, stream_outputs, interval, self.unit.host.sample_rate)

    def _render_one_intersection(self, intersection: ClipIntersection, stream_outputs: List[np.ndarray],
                                 interval: TimeInterval,
                                 sample_rate: int):

        clip: AudioClip = cast(AudioClip, intersection.clip)
        wav_data = self._get_processed_wav_data(clip)

        if wav_data.num_channels != 1:
            # number of channels should match it not a mono sample
            if wav_data.num_channels != len(stream_outputs):
                raise Exception(
                    f"""number of channels in wav_data {wav_data.num_channels}
                    and in output {len(stream_outputs)} does not match. Related file: {clip.source_file_path}""")

        if intersection.start_clip_time is None:
            raise Exception('intersection is missing start clip time prop')

        patch_start_in_wav_data_in_samples: int = round(clip.cue_sample + intersection.start_clip_time * sample_rate)

        if patch_start_in_wav_data_in_samples > wav_data.length_in_samples():
            return

        if intersection.end_clip_time is None:
            raise Exception('intersection is missing end clip time prop')

        patch_end_in_wav_data_in_samples: int = min(
            round(clip.cue_sample + intersection.end_clip_time * sample_rate),
            wav_data.length_in_samples())

        if intersection.start_project_time is None:
            raise Exception('intersection is missing start project time')

        patch_start_in_output_in_samples: int = round(
            (intersection.start_project_time - interval.start_in_seconds) * sample_rate)

        patch_length_in_samples: int = patch_end_in_wav_data_in_samples - patch_start_in_wav_data_in_samples
        patch_end_in_output_in_samples: int = patch_start_in_output_in_samples + patch_length_in_samples

        patch_length_in_wav_data = patch_end_in_wav_data_in_samples - patch_start_in_wav_data_in_samples
        patch_length_in_output = patch_end_in_output_in_samples - patch_start_in_output_in_samples

        if patch_length_in_wav_data != patch_length_in_output:
            raise Exception(
                f"""patch lengths in sample and in interval diff. In sample: {patch_length_in_wav_data},
                in interval: {patch_length_in_output}""")

        for i, output in enumerate(stream_outputs):
            if wav_data.num_channels > 1:
                channel_in_wav = wav_data.data[i]
            else:
                # mono samples is a special case - we add their single channel uniformly to all outputs
                channel_in_wav = wav_data.data[0]

            # slicing returns a view, so it must be efficient
            patch_data: np.ndarray = channel_in_wav[patch_start_in_wav_data_in_samples:patch_end_in_wav_data_in_samples]
            patched_data: np.ndarray = output[patch_start_in_output_in_samples:patch_end_in_output_in_samples]

            if patch_data.shape != patched_data.shape:
                raise Exception(f"""patch and patched have different shapes.
                patch: {str(patch_data.shape)}
                patched: {str(patched_data.shape)}
                """)

            np.add(patch_data, patched_data, out=patched_data)

    def _get_processed_wav_data(self, clip: AudioClip) -> ProcessedWavData:
        cache_key: str = self._generate_cache_key(clip)
        if cache_key not in self._processed_wav_data_cache:
            self._processed_wav_data_cache[cache_key] = self._generate_processed_wav_data(clip)

        return self._processed_wav_data_cache[cache_key]

    def _generate_cache_key(self, clip: AudioClip) -> str:
        return clip.source_file_path + "_" + str(clip.rate)

    def _generate_processed_wav_data(self, clip: AudioClip) -> ProcessedWavData:

        raw_waveform = self.wave_data_provider.get_wave_data_by_file_path(clip.source_file_path)
        (sample_rate, data) = (raw_waveform.sample_rate, raw_waveform.data)

        # in the future, this will involve not just reading the wav file, but also
        # converting it into host's sample rate (self.unit.hot.sample_rate),
        # and taking into account clip's rate property.
        # Also reading non-wav files.

        # that's why Sample does not have sample rate property as it is already expected
        # to be in host's one

        return ProcessedWavData(
            data=data,
            sample_rate=sample_rate
        )

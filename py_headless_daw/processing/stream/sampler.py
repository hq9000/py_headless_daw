from typing import List, cast

import numpy as np

from py_headless_daw.project.content.audio_clip import AudioClip
from py_headless_daw.schema.clip_track_processing_strategy import ClipTrackProcessingStrategy
from py_headless_daw.schema.dto.time_interval import TimeInterval
from py_headless_daw.schema.events.event import Event
from py_headless_daw.schema.processing_strategy import ProcessingStrategy
import wave
import scipy.io.wavfile

from py_headless_daw.services.waveform_provider_interface import WaveformProviderInterface
from py_headless_daw.shared.clip_intersection import ClipIntersection


class ProcessedWavData:
    def __init__(self, data: np.ndarray):
        self.uncompressed_data: np.ndarray = data


class Sampler(ClipTrackProcessingStrategy):
    """
    Sampler is a strategy that produces audio basing on the number of associated AudioClips
    """

    _processed_wav_data_cache = {}

    def __init__(self, clips: List[AudioClip], wave_data_provider: WaveformProviderInterface):
        super().__init__(clips)
        for clip in clips:
            if not isinstance(clip, AudioClip):
                raise Exception(f"a clips was expected to be an AudioClip, instead it is {type(clip)}")
        self.clips: List[AudioClip] = clips
        self.wave_data_provider: WaveformProviderInterface = wave_data_provider

    def render(self, interval: TimeInterval, stream_inputs: List[np.ndarray], stream_outputs: List[np.ndarray],
               event_inputs: List[List[Event]], event_outputs: List[List[Event]]):
        intersections = self._find_intersections(interval)

        for intersection in intersections:
            self._render_one_intersection(intersection, stream_outputs, self.unit.host.sample_rate)

    def _render_one_intersection(self, intersection: ClipIntersection, stream_outputs: List[np.ndarray],
                                 sample_rate: int):
        clip: AudioClip = cast(AudioClip, intersection.clip)
        wav_data = self._get_processed_wav_data(clip)

        if len(wav_data.uncompressed_data) != len(stream_outputs):
            raise Exception(
                f"number of channels in wav_data {len(wav_data.uncompressed_data)} \
                and in output {len(stream_outputs)} does not match. Related file: {clip.source_file_path}")

        patch_start_in_wav_data: int = round(clip.cue_sample + intersection.start_clip_time * sample_rate)
        patch_start_in_output: int = # to be continued

        # to be continued
        # also check how we can use "DI injector" http://python-dependency-injector.ets-labs.org/
        # idea: wav data provider service to make it easily mockable (probably an overkill though). to be checked
        patch_length: int

        patch_data: np.ndarray = self._get_patch_data(intersection, self.)

    def _get_processed_wav_data(self, clip: AudioClip) -> ProcessedWavData:
        cache_key: str = self._generate_cache_key(clip)
        if self._processed_wav_data_cache[cache_key] is None:
            self._processed_wav_data_cache[cache_key] = self._generate_processed_wav_data(clip)

        return self._processed_wav_data_cache[cache_key]

    def _generate_cache_key(self, clip: AudioClip) -> str:
        return clip.source_file_path + str(clip.rate)

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
            data=data
        )

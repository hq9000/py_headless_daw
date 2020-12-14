import unittest
from typing import List, Tuple, Optional

import numpy as np
import parametrized

from py_headless_daw.dto.waveform import Waveform
from py_headless_daw.processing.stream.sampler import Sampler
from py_headless_daw.project.content.audio_clip import AudioClip
from py_headless_daw.schema.dto.time_interval import TimeInterval
from py_headless_daw.schema.host import Host
from py_headless_daw.schema.unit import Unit
from py_headless_daw.services.wave_data_provider import WaveformProviderInterface


class MockedWaveformProvider(WaveformProviderInterface):

    def get_wave_data_by_file_path(self, file_path: str) -> Waveform:
        """
        interprets the file path as:

        numchannels_volume_lengthinsamples_samplerate, e.g. 2_0.123_100_44100 and generates a flat "wave"
        of the given length (in samples) on a given sample rate

        """

        (num_channels, volume, length_in_samples, sample_rate) = self._parse_file_path(file_path)
        data = np.zeros((num_channels, length_in_samples)) + volume
        return Waveform(sample_rate, data)

    def _parse_file_path(self, file_path: str) -> Tuple[int, float, int, int]:
        elements = file_path.split('_')
        if len(elements) != 4:
            raise Exception('the file path should have had exactly 3 underscore-delimited parts')

        (num_channels, volume, length_in_samples, sample_rate) = (
            int(elements[0]),
            float(elements[1]),
            int(elements[2]),
            int(elements[3])
        )

        return num_channels, volume, length_in_samples, sample_rate


@parametrized.parametrized_test_case
class SamplerTest(unittest.TestCase):

    @parametrized.parametrized([
        [0.0, 1.0, 100, 1.0, None],
        [1.0, 2.0, 100, 0.0, None],
        [2.0, 3.0, 100, 2.0, None],
        [3.0, 4.0, 100, 0.0, None],
        [0.5, 1.5, 100, None, 0.5],
        [0.75, 1.75, 100, None, 0.25],
        [10.0, 11.0, 100, None, 0.5],  # clip goes beyond underlying file
        [13.0, 14.0, 100, 1.0, None],  # single-channel clip
    ])
    def one_case(self, interval_start: float, interval_end: float, buffer_length: int,
                 expected_level_in_output: Optional[float], expected_average: Optional[float]):
        host = Host()
        host.sample_rate = 100

        unit = Unit(2, 0, 2, 0, host)

        clips: List[AudioClip] = self.generate_test_clips()
        mocked_waveform_provider = MockedWaveformProvider()
        strategy = Sampler(clips, mocked_waveform_provider)
        strategy.unit = unit

        interval = TimeInterval()
        interval.start_in_seconds = interval_start
        interval.end_in_seconds = interval_end

        out1 = np.zeros(shape=(buffer_length,), dtype=np.float32)
        out2 = np.zeros(shape=(buffer_length,), dtype=np.float32)

        strategy.render(interval, [], [out1, out2], [], [])

        values_tested: bool = False

        if expected_level_in_output is not None:
            expected_buffer = np.zeros(100, ) + expected_level_in_output
            self.assertTrue((out1 == expected_buffer).all())
            values_tested = True

        if expected_average is not None:
            self.assertEqual(expected_average, np.mean(out1))
            self.assertEquals(expected_average, np.mean(out2))
            values_tested = True

        self.assertTrue(values_tested)

    def generate_test_clips(self) -> List[AudioClip]:
        clip1 = AudioClip(0.0, 1.0, "2_1.0_1000_100", 0, 1.0)

        clip2 = AudioClip(2.0, 3.0, "2_1.0_1000_100", 0, 1.0)
        clip3 = AudioClip(2.0, 3.0, "2_1.0_1000_100", 0, 1.0)

        clip4 = AudioClip(10.0, 11.0, "2_1.0_1000_100", 950, 1.0)

        clip5 = AudioClip(13.0, 14.0, "1_1.0_1000_100", 0, 1.0)

        return [clip1, clip2, clip3, clip4, clip5]

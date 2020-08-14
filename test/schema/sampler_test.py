import unittest
from typing import List, Tuple

import numpy as np

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

        pass


class SamplerTest(unittest.TestCase):
    def test_something(self):
        host = Host()
        host.sample_rate = 100

        unit = Unit(2, 0, 2, 0, host)

        clips: List[AudioClip] = self.generate_test_clips()
        mocked_waveform_provider = MockedWaveformProvider()
        strategy = Sampler(clips, mocked_waveform_provider)
        strategy.unit = unit

        interval = TimeInterval()
        interval.start_in_seconds = 0.0
        interval.end_in_seconds = 1.0

        out1 = np.zeros(shape=(100,), dtype=np.float32)
        out2 = np.zeros(shape=(100,), dtype=np.float32)

        strategy.render(interval, [], [out1, out2], [], [])

        self.assertTrue((out1 == np.ones((100,))).all())

    def generate_test_clips(self) -> List[AudioClip]:
        clip1 = AudioClip(0.0, 1.0, "2_1.0_1000_100", 0, 1.0)

        clip2 = AudioClip(2.0, 3.0, "2_1.0_1000_100", 0, 1.0)
        clip3 = AudioClip(2.0, 3.0, "2_1.0_1000_100", 0, 1.0)

        return [clip1, clip2, clip3]

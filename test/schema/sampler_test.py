import unittest
from typing import List

from py_headless_daw.dto.waveform import Waveform
from py_headless_daw.processing.stream.sampler import Sampler
from py_headless_daw.project.content.audio_clip import AudioClip
from py_headless_daw.schema.dto.time_interval import TimeInterval
from py_headless_daw.schema.host import Host
from py_headless_daw.schema.unit import Unit
from py_headless_daw.services.wave_data_provider import WaveformProviderInterface

class MockedWaveformProvider(WaveformProviderInterface):

    def get_wave_data_by_file_path(self, file_path: str) -> Waveform:
        file_path.split('_')

        # continue on this mock



class SamplerTest(unittest.TestCase):
    def test_something(self):
        host = Host()
        host.sample_rate = 100

        unit = Unit(2, 0, 2, 0, host)

        clips: List[AudioClip] = self.generate_test_clips()
        mocked_waveform_provider = self.create_mocked_waveform_provider()
        strategy = Sampler(clips, mocked_waveform_provider)
        strategy.unit = unit

        interval = TimeInterval()
        interval.start_in_seconds = 0
        interval.end_in_seconds = 1



    def generate_test_clips(self) -> List[AudioClip]:
        pass

    def create_mocked_waveform_provider(self) -> WaveformProviderInterface:




        pass

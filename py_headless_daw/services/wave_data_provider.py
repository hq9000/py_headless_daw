from abc import ABC, abstractmethod

import scipy.io.wavfile

from py_headless_daw.dto.waveform import Waveform


class WaveformProviderInterface(ABC):

    @abstractmethod
    def get_wave_data_by_file_path(self, file_path: str) -> Waveform:
        pass


class WaveDataProvider(WaveformProviderInterface):
    """
    Gets waveforms from different sources, such as local files.
    The result is a Waveform object.
    """

    def get_wave_data_by_file_path(self, file_path: str) -> Waveform:
        (sample_rate, data) = scipy.io.wavfile.read(file_path)
        return Waveform(sample_rate, data)

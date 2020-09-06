from abc import ABC, abstractmethod

import scipy.io.wavfile
import numpy as np

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
        data = np.rot90(data)

        divider = None
        if data.dtype is np.dtype(np.int16):
            divider = 32768
        elif data.dtype is np.dtype(np.int32):
            divider = 2147483648

        if divider is not None:
            float_data = data / divider
            data = float_data.astype(np.float32)

        return Waveform(sample_rate, data)

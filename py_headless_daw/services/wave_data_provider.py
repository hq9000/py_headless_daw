from abc import ABC, abstractmethod
from typing import Tuple

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
        wav_file_details: Tuple[int, np.ndarray] = scipy.io.wavfile.read(file_path)
        (sample_rate, data) = wav_file_details

        if data.ndim > 1:
            data = np.rot90(data)
        else:
            data = data.reshape((1, data.shape[0]))

        divider = None
        if data.dtype is np.dtype(np.int16):
            divider = 32768
        elif data.dtype is np.dtype(np.int32):
            divider = 2147483648

        if divider is not None:
            float_data = data / divider
            data = float_data.astype(np.float32)

        return Waveform(sample_rate, data)

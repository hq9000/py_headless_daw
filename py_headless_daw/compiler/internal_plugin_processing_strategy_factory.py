import numpy as np

from py_headless_daw.compiler.compiler_exception import CompilerException
from py_headless_daw.processing.stream.sampler import Sampler
from py_headless_daw.processing.stream.stereo_panner import StereoPanner
from py_headless_daw.processing.stream.stream_gain import StreamGain
from py_headless_daw.project.plugins.internal_plugin import GainPlugin, PanningPlugin, SamplerPlugin
from py_headless_daw.schema.processing_strategy import ProcessingStrategy
from py_headless_daw.services.wave_data_provider import WaveformProviderInterface
from py_headless_daw.project.plugins.internal_plugin import InternalPlugin as InternalProjectPlugin


class InternalPluginProcessingStrategyFactory:

    def __init__(self, waveform_provider: WaveformProviderInterface):
        self._waveform_provider: WaveformProviderInterface = waveform_provider

    # noinspection PyMethodMayBeStatic
    def produce(self, plugin: InternalProjectPlugin) -> ProcessingStrategy:

        if isinstance(plugin, GainPlugin):
            return StreamGain(np.float32(1.0))
        elif isinstance(plugin, PanningPlugin):
            return StereoPanner(np.float32(0.0))
        elif isinstance(plugin, SamplerPlugin):
            return Sampler(plugin.clips, self._waveform_provider)
        else:
            raise CompilerException(
                "I don't know how to produce a processing strategy for internal plugin of type " + str(type(plugin)))

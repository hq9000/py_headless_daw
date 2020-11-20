import numpy as np

from py_headless_daw.compiler.compiler_exception import CompilerException
from py_headless_daw.processing.hybrid.drum_synth_strategy import DrumSynthStrategy
from py_headless_daw.processing.stream.sampler import Sampler
from py_headless_daw.processing.stream.stereo_panner import StereoPanner
from py_headless_daw.processing.stream.stream_gain import StreamGain
from py_headless_daw.project.audio_track import AudioTrack
from py_headless_daw.project.plugins.drum_synth_plugin import DrumSynthPlugin
from py_headless_daw.project.plugins.internal_plugin import GainPlugin, PanningPlugin, SamplerPlugin
from py_headless_daw.project.track import Track
from py_headless_daw.schema.processing_strategy import ProcessingStrategy
from py_headless_daw.services.wave_data_provider import WaveformProviderInterface
from py_headless_daw.project.plugins.internal_plugin import InternalPlugin as InternalProjectPlugin


class InternalPluginProcessingStrategyFactory:

    def __init__(self, waveform_provider: WaveformProviderInterface):
        self._waveform_provider: WaveformProviderInterface = waveform_provider

    # noinspection PyMethodMayBeStatic
    def produce(self, plugin: InternalProjectPlugin, track: Track) -> ProcessingStrategy:

        if isinstance(track, AudioTrack):
            overall_track_gain_value = track.get_gain_parameter().value
            overall_track_panning_value = track.get_panning_parameter().value

            if isinstance(plugin, GainPlugin):
                return StreamGain(np.float32(overall_track_gain_value))
            elif isinstance(plugin, PanningPlugin):
                return StereoPanner(np.float32(overall_track_panning_value))
            elif isinstance(plugin, SamplerPlugin):
                return Sampler(plugin.clips, self._waveform_provider)
            elif isinstance(plugin, DrumSynthPlugin):
                return self._construct_drum_synth_plugin(plugin)
            else:
                raise CompilerException(
                    "I don't know how to produce a processing strategy for internal plugin of type " + str(
                        type(plugin)))
        else:
            raise CompilerException(
                "I don't know how to compile internal plugins for this kind of tracks (error: 9029b61c)")

    def _construct_drum_synth_plugin(self, plugin: DrumSynthPlugin) -> DrumSynthStrategy:
        return DrumSynthStrategy(plugin)

from typing import List, Dict, Optional, Callable, cast

from py_headless_daw.compiler.internal_plugin_processing_strategy_factory import InternalPluginProcessingStrategyFactory
from py_headless_daw.processing.event.midi_track_strategy import MidiTrackStrategy
from py_headless_daw.processing.event.value_provider_based_event_emitter import ValueProviderBasedEventEmitter
from py_headless_daw.processing.hybrid.vst_plugin import VstPlugin as VstPluginProcessingStrategy
from py_headless_daw.project.audio_track import AudioTrack
from py_headless_daw.project.midi_track import MidiTrack
from py_headless_daw.project.parameter import Parameter
from py_headless_daw.project.plugins.internal_plugin import InternalPlugin as InternalProjectPlugin
from py_headless_daw.project.plugins.plugin import Plugin
from py_headless_daw.project.plugins.vst_plugin import VstPlugin as VstProjectPlugin
from py_headless_daw.project.project import Project
from py_headless_daw.project.track import Track
from py_headless_daw.schema.chain import Chain
from py_headless_daw.schema.events.event import Event
from py_headless_daw.schema.events.parameter_value_event import ParameterValueEvent
from py_headless_daw.schema.host import Host
from py_headless_daw.schema.unit import Unit
from py_headless_daw.schema.wiring import StreamNode, Connector


class ProjectCompiler:

    def __init__(self, internal_plugin_processing_strategy_factory: InternalPluginProcessingStrategyFactory):
        self._internal_plugin_processing_strategy_factory: InternalPluginProcessingStrategyFactory = \
            internal_plugin_processing_strategy_factory

    def compile(self, project: Project) -> List[StreamNode]:
        """
        Given a project, returns a list of stream nodes (as many nodes as many channels
        there are - e.g. 2 for stereo.

        Then the user is expected to iteratively render data from those nodes into buffers.

        :param project: Project
        :return: List[StreamNode]
        """

        # this one is to keep track of compiler tracks to properly handle cycles
        compiled_tracks: Dict[Track, Unit] = {}

        host = Host()

        master_unit = self._compile_internal(host, project, project.master_track, compiled_tracks)
        return master_unit.output_stream_nodes

    def _compile_internal(self, host: Host, project: Project, track: Track, compiled_tracks: Dict[Track, Unit]) -> Unit:
        """
        compiles the "track itself" and then descends to its inputs
        """

        this_track_unit: Unit = self._compile_track_itself(host, project, track, compiled_tracks)

        for input_track in track.inputs:
            input_unit = self._compile_internal(host, project, input_track, compiled_tracks)
            self._connect_units(input_unit, this_track_unit)

        return this_track_unit

    def _compile_track_itself(self, host: Host, project: Project, track: Track,
                              compiled_tracks: Dict[Track, Unit]) -> Unit:
        """
        non-recursively compiles a track

        :param track: Track
        :param compiled_tracks: Dict[Track,Unit]
        :return:
        """
        if track in compiled_tracks:
            return compiled_tracks[track]
        if isinstance(track, MidiTrack):
            res = self._compile_midi_track_itself(host, project, track)
        elif isinstance(track, AudioTrack):
            res = self._compile_audio_track_itself(host, project, cast(AudioTrack, track))
        else:
            raise Exception(f'don\'t know how to compile this type of track: {str(type(track))}')

        compiled_tracks[track] = res
        return res

    @classmethod
    def _connect_units(cls, source: Unit, destination: Unit):
        for i, source_stream_node in enumerate(source.output_stream_nodes):
            output_stream_node = destination.input_stream_nodes[i]
            if not Connector.connected(source_stream_node, output_stream_node):
                Connector(source_stream_node, output_stream_node)

        for i, source_event_node in enumerate(source.output_event_nodes):
            output_event_node = destination.input_event_nodes[i]
            if not Connector.connected(source_event_node, output_event_node):
                Connector(source_event_node, output_event_node)

    # noinspection PyUnusedLocal
    @staticmethod
    def _compile_midi_track_itself(host: Host, project: Project, track: MidiTrack) -> Unit:
        strategy = MidiTrackStrategy(track)
        unit = Unit(0, 0, 0, 1, host, strategy)
        unit.name = "midi track"
        return unit

    def _compile_audio_track_itself(self, host: Host, project: Project, track: AudioTrack) -> Chain:

        previous_unit: Optional[Unit] = None
        first_unit: Optional[Unit] = None
        last_unit: Optional[Unit] = None

        for number, plugin in enumerate(track.plugins):
            last_unit = self._create_audio_plugin_unit(host, project, plugin, track)
            if 0 == number:
                first_unit = last_unit
            if previous_unit is not None:
                self._connect_units(previous_unit, last_unit)
            previous_unit = last_unit

        if first_unit is None or last_unit is None:
            raise Exception('first_unit and/or last_unit are not defined')

        res = Chain(first_unit, last_unit)
        res.name = track.name
        return res

    def _create_audio_plugin_unit(self, host: Host, project: Project, plugin: Plugin, track: Track) -> Unit:

        main_unit: Unit

        if isinstance(plugin, VstProjectPlugin):
            main_unit = self._create_vst_audio_plugin_unit(host, project, plugin, track)
        elif isinstance(plugin, InternalProjectPlugin):
            main_unit = self._create_internal_plugin_unit(host, project, plugin, track)
        else:
            raise Exception('do not know how to treat project plugins of class ' + type(plugin).__name__)

        for parameter in plugin.parameters:
            if parameter.value_provider is not None:
                def parameter_value_transformer(value: float, sample_position: int) -> ParameterValueEvent:
                    # the "parameter" is enclosed from the outer scope
                    return ParameterValueEvent(sample_position, parameter.name, value)

                value_event_emitter_unit: Unit = self._create_unit_for_parameter_value_emission(
                    host,
                    parameter,
                    parameter_value_transformer)

                Connector(value_event_emitter_unit.output_event_nodes[0], main_unit.input_event_nodes[0])

        return main_unit

    @classmethod
    def _create_vst_audio_plugin_unit(cls, host: Host, project: Project, plugin: VstProjectPlugin,
                                      track: Track) -> Unit:
        if plugin.is_synth:
            num_input_event_channels = 1
            num_input_stream_channels = 0
            num_output_event_channels = 0
            num_output_stream_channels = project.num_audio_channels
        else:
            num_input_event_channels = 1  # for envelopes in the future
            num_input_stream_channels = project.num_audio_channels
            num_output_event_channels = 0
            num_output_stream_channels = project.num_audio_channels

        unit = Unit(num_input_stream_channels, num_input_event_channels, num_output_stream_channels,
                    num_output_event_channels, host)

        strategy = cls._create_vst_plugin_processing_strategy(plugin.path_to_shared_library, unit, plugin)
        unit.set_processing_strategy(strategy)
        unit.name = track.name + " - " + plugin.name
        return unit

    def _create_internal_plugin_unit(self, host: Host, project: Project, plugin: InternalProjectPlugin,
                                     track: Track) -> Unit:
        strategy = self._internal_plugin_processing_strategy_factory.produce(plugin, track)

        num_input_event_channels = 1
        num_input_stream_channels = project.num_audio_channels
        num_output_event_channels = 1
        num_output_stream_channels = project.num_audio_channels

        unit = Unit(num_input_stream_channels, num_input_event_channels, num_output_stream_channels,
                    num_output_event_channels, host, strategy)

        unit.name = track.name + ' - ' + type(strategy).__name__
        return unit

    @classmethod
    def _create_unit_for_parameter_value_emission(cls, host: Host, parameter: Parameter,
                                                  transformer_function: Callable[
                                                      [float, int], Event]) -> Unit:
        if parameter.value_provider is None:
            raise Exception('value_provider is None')

        strategy = ValueProviderBasedEventEmitter(parameter.value_provider, transformer_function)
        res = Unit(0, 0, 0, 1, host, strategy)

        res.name = "parameter emitter for %s" % (parameter.name,)

        return res

    @classmethod
    def _create_parameter_value_transformer_function(cls, parameter, plugin) -> Callable[[float], Event]:
        pass

    @classmethod
    def _create_vst_plugin_processing_strategy(cls, path_to_shared_lib: str, unit: Unit, plugin: VstProjectPlugin):

        path_to_shared_lib_as_bytes: bytes = path_to_shared_lib.encode('utf-8')
        strategy = VstPluginProcessingStrategy(path_to_shared_lib_as_bytes, unit)

        for parameter in plugin.parameters:
            strategy.set_parameter_value(parameter.name, parameter.value)

        return strategy

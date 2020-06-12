from typing import List, Dict, Optional

from py_headless_daw.processing.hybrid.vst_plugin import VstPlugin as VstPluginProcessingStrategy
from py_headless_daw.project.audio_track import AudioTrack
from py_headless_daw.project.midi_track import MidiTrack
from py_headless_daw.project.plugins.internal_plugin import InternalPlugin as InternalProjectPlugin
from py_headless_daw.project.plugins.plugin import Plugin
from py_headless_daw.project.plugins.vst_plugin import VstPlugin as VstProjectPlugin
from py_headless_daw.project.project import Project
from py_headless_daw.project.track import Track
from py_headless_daw.schema.chain import Chain
from py_headless_daw.schema.host import Host
from py_headless_daw.schema.unit import Unit
from py_headless_daw.schema.wiring import StreamNode, Connector


class ProjectCompiler:
    def compile(self, project: Project) -> List[StreamNode]:
        """
        Given a project, returns a list of stream nodes (as many nodes as many channels
        there are - e.g. 2 for stereo.

        Then the user is expected to iteratively render data from those nodes into buffers.

        :param project: Project
        :return: List[StreamNode]
        """

        compiled_tracks: Dict[Track, Unit] = {}

        host = Host()

        master_unit = self._compile_internal(host, project, project.master_track, compiled_tracks)
        return master_unit.output_stream_nodes

    def _compile_internal(self, host: Host, project: Project, track: Track, compiled_tracks: Dict[Track, Unit]) -> Unit:
        this_track_unit: Unit = self._compile_track_itself(host, project, track, compiled_tracks)

        for input_track in track.inputs:
            input_unit = self._compile_internal(host, project, input_track, compiled_tracks)
            self._connect_units(input_unit, this_track_unit)

        return this_track_unit

    def _compile_track_itself(self, host: Host, project: Project, track: Track, compiled_tracks: Dict[Track, Unit]) -> Unit:
        """
        non-recursively compiles a track

        :param track: Track
        :param compiled_tracks: Dict[Track,Unit]
        :return:
        """
        if track in compiled_tracks:
            return compiled_tracks[track]

        if isinstance(track, MidiTrack):
            return self._compile_midi_track_itself(host, project, track)
        elif isinstance(track, AudioTrack):
            return self._compile_audio_track_itself(host, project, track)

    @classmethod
    def _connect_units(cls, source: Unit, destination: Unit):
        for i, source_stream_node in enumerate(source.output_stream_nodes):
            output_node = destination.input_stream_nodes[i]
            Connector(source_stream_node, output_node)

        for i, source_event_node in enumerate(source.output_event_nodes):
            output_node = destination.output_event_nodes[i]
            Connector(source_event_node, output_node)

    @staticmethod
    def _compile_midi_track_itself(host: Host, project: Project, track: MidiTrack) -> Unit:

        pass

    @classmethod
    def _compile_audio_track_itself(cls, host: Host, project: Project, track: AudioTrack) -> Chain:

        previous_unit: Optional[Unit] = None
        first_unit: Optional[Unit] = None
        last_unit: Optional[Unit] = None
        for number, plugin in enumerate(track.plugins):
            last0_unit = cls._create_audio_plugin_unit(host, project, plugin)
            if 1 == number:
                first_unit = last_unit
            if previous_unit is not None:
                cls._connect_units(previous_unit, last_unit)

        return Chain(first_unit, last_unit)

    @classmethod
    def _create_audio_plugin_unit(cls, host: Host, project: Project, plugin: Plugin) -> Unit:
        if isinstance(plugin, VstProjectPlugin):
            return cls._create_vst_audio_plugin_unit(host, project, plugin)
        elif isinstance(plugin, InternalProjectPlugin):
            return cls._create_internal_plugin_unit(host, project, plugin)
        else
            raise Exception('do not know how to treat project plugins of class ' + type(plugin).__name__)

    @classmethod
    def _create_vst_audio_plugin_unit(cls, host: Host, project: Project, plugin: VstProjectPlugin) -> Unit:
        path_to_shared_lib: bytes = plugin.path_to_shared_library.encode('utf-8')

        strategy = VstPluginProcessingStrategy(path_to_shared_lib)

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

        return Unit(num_input_stream_channels, num_input_event_channels, num_output_stream_channels,
                    num_output_event_channels, host, strategy)

    @classmethod
    def _create_internal_plugin_unit(cls, host: Host, project: Project, plugin: InternalProjectPlugin):
        strategy = cls._create_strategy_for_internal_plugin(host, project, plugin)
        # todo
        pass

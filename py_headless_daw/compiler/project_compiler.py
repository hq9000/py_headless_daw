from typing import List, Dict

from py_headless_daw.project.audio_track import AudioTrack
from py_headless_daw.project.midi_track import MidiTrack
from py_headless_daw.project.project import Project
from py_headless_daw.project.track import Track
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

        master_unit = self._compile_internal(project.master_track, compiled_tracks)
        return master_unit.output_stream_nodes

    def _compile_internal(self, track: Track, compiled_tracks: Dict[Track, Unit]) -> Unit:
        this_track_unit: Unit = self._compile_track_itself(track, compiled_tracks)

        for input_track in track.inputs:
            input_unit = self._compile_internal(input_track, compiled_tracks)
            self._connect_units(input_unit, this_track_unit)

        return this_track_unit

    def _compile_track_itself(self, track: Track, compiled_tracks: Dict[Track, Unit]) -> Unit:
        """
        non-recursively compiles a track

        :param track: Track
        :param compiled_tracks: Dict[Track,Unit]
        :return:
        """
        if track in compiled_tracks:
            return compiled_tracks[track]

        if isinstance(track, MidiTrack):
            return self._compile_midi_track_itself(track)
        elif isinstance(track, AudioTrack):
            return self._compile_audio_track_itself(track)

    @staticmethod
    def _connect_units(source: Unit, destination: Unit):
        for i, source_stream_node in enumerate(source.output_stream_nodes):
            output_node = destination.input_stream_nodes[i]
            Connector(source_stream_node, output_node)

        for i, source_event_node in enumerate(source.output_event_nodes):
            output_node = destination.output_event_nodes[i]
            Connector(source_event_node, output_node)

    @staticmethod
    def _compile_midi_track_itself(track: MidiTrack) -> Unit:

        pass

    @staticmethod
    def _compile_audio_track_itself(track: AudioTrack) -> Unit:

        pass

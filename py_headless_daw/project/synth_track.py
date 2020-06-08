from py_headless_daw.project.audio_track import AudioTrack
from py_headless_daw.project.exceptions import RoutingException


class SynthTrack(AudioTrack):

    def add_output(self, output: AudioTrack):
        if not type(output) is AudioTrack:
            raise RoutingException('SynthTracks can only be outputted to AudioTracks')

        super().add_output(output)

import unittest

from py_headless_daw.project.audio_track import AudioTrack


class TrackTest(unittest.TestCase):
    def test_audio_track(self):
        track = AudioTrack()
        self.assertEqual(2, len(track.parameters))
        self.assertEqual(2, len(track.plugins))

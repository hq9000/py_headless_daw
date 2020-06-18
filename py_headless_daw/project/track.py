from typing import List

from py_headless_daw.project.having_parameters import HavingParameters


class Track(HavingParameters):
    def __init__(self):
        super().__init__()

        self.outputs = []  # type: List[Track]
        self.inputs = []  # type: List[Track]
        self.name: str = 'unnamed'

    def add_input(self, input_track):
        self.inputs.append(input_track)

    def add_output(self, output_track):
        # type: (Track)->None
        self.outputs.append(output_track)
        output_track.inputs.append(self)

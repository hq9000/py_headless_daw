from math import ceil
from typing import List

from scipy.io import wavfile

from py_headless_daw.compiler.project_compiler import ProjectCompiler
from py_headless_daw.project.project import Project
from py_headless_daw.schema.dto.time_interval import TimeInterval
from py_headless_daw.schema.wiring import StreamNode

import numpy as np


class ProjectRenderer:
    SAMPLE_RATE = 44100

    def __init__(self, project_compiler: ProjectCompiler):
        self._compiler: ProjectCompiler = project_compiler

    def render_to_file(self, project: Project, start_time: float, end_time: float, out_file_path: str):
        buffer = self.render_to_array(project, start_time, end_time)
        buffer = np.rot90(buffer, k=-1)
        wavfile.write(out_file_path, self.SAMPLE_RATE, buffer)

    def render_to_array(self, project: Project, start_time: float, end_time: float) -> np.ndarray:
        output_stream_nodes: List[StreamNode] = self._compiler.compile(project)

        left_node = output_stream_nodes[0]
        right_node = output_stream_nodes[1]

        buffer_length_samples = 4410
        sample_rate = self.SAMPLE_RATE

        buffer_length_seconds = buffer_length_samples / sample_rate
        num_frames = ceil((end_time - start_time) / buffer_length_seconds)

        result_buffer = np.ndarray(shape=(2, num_frames * buffer_length_samples), dtype=np.float32)

        left_frame_buffer = np.ndarray(shape=(buffer_length_samples,), dtype=np.float32)
        right_frame_buffer = np.ndarray(shape=(buffer_length_samples,), dtype=np.float32)

        for i in range(num_frames):
            interval = TimeInterval()

            interval.num_samples = buffer_length_samples
            interval.start_in_seconds = start_time + i * buffer_length_seconds
            interval.end_in_seconds = interval.start_in_seconds + buffer_length_seconds

            left_node.render(interval, left_frame_buffer)
            right_node.render(interval, right_frame_buffer)

            start_sample_in_result = i * buffer_length_samples
            end_sample_in_result = start_sample_in_result + buffer_length_samples

            result_buffer[0][start_sample_in_result:end_sample_in_result] = left_frame_buffer
            result_buffer[1][start_sample_in_result:end_sample_in_result] = right_frame_buffer

        return result_buffer

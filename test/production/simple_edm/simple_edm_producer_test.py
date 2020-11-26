import unittest
from pathlib import Path
from py_headless_daw.application_container import ApplicationContainer
from py_headless_daw.production.seed import Seed
from py_headless_daw.production.simple_edm.simple_edm_producer import SimpleEdmProducer
from py_headless_daw.project.project_renderer import ProjectRenderer

import matplotlib.pyplot as plt


class MyTestCase(unittest.TestCase):
    def test_something(self):
        seed = Seed('hello')
        producer = SimpleEdmProducer(seed)
        project = producer.generate_project()

        container = ApplicationContainer()

        compiler = container.project_compiler()
        renderer = ProjectRenderer(compiler)

        out_file_path = str(Path(__file__).parent.absolute()) + "/output/out.wav"
        renderer.render_to_file(project, project.start_time_seconds, project.end_time_seconds, out_file_path)

        #plt.plot(output[1][0:400000])
        #plt.show()

        pass


if __name__ == '__main__':
    unittest.main()

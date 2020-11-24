import unittest

from py_headless_daw.application_container import ApplicationContainer
from py_headless_daw.production.seed import Seed
from py_headless_daw.production.simple_edm.simple_edm_producer import SimpleEdmProducer
from py_headless_daw.project.project_renderer import ProjectRenderer


class MyTestCase(unittest.TestCase):
    def test_something(self):
        seed = Seed('hello')
        producer = SimpleEdmProducer(seed)
        project = producer.generate_project()

        container = ApplicationContainer()

        compiler = container.project_compiler()
        renderer = ProjectRenderer(compiler)

        renderer.render_to_array(project, project.start_time_seconds, project.end_time_seconds)


if __name__ == '__main__':
    unittest.main()

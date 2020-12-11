from pathlib import Path

from py_headless_daw.application_container import ApplicationContainer
from py_headless_daw.production.seed import Seed
from py_headless_daw.production.simple_edm.simple_edm_producer import SimpleEdmProducer
from py_headless_daw.project.project_renderer import ProjectRenderer

seed = Seed('hello1')
producer = SimpleEdmProducer(seed)
project = producer.generate_project()

container = ApplicationContainer()

compiler = container.project_compiler()
renderer = ProjectRenderer(compiler)

out_file_path = str(Path(__file__).parent.absolute()) + "/output/out.wav"

if project.start_time_seconds is None:
    raise ValueError()

if project.end_time_seconds is None:
    raise ValueError()

renderer.render_to_file(project, project.start_time_seconds, project.end_time_seconds, out_file_path)

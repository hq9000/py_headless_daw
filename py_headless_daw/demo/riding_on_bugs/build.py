import logging

from py_headless_daw.application_container import ApplicationContainer
from py_headless_daw.demo.riding_on_bugs.riding_on_bugs import RidingOnBugs
from pathlib import Path


def set_up_logging(level):
    root_logger = logging.getLogger()
    handler = logging.StreamHandler()
    root_logger.addHandler(handler)

    root_logger.setLevel(level)
    handler.setLevel(level)


if __name__ == '__main__':

    set_up_logging(logging.DEBUG)

    container = ApplicationContainer()

    demo = RidingOnBugs(container.project_renderer())
    out_file = str(Path(__file__).parent.absolute()) + "/output/out.wav"
    demo.render(out_file)

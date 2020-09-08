import logging

from py_headless_daw.project.project import Project
from py_headless_daw.project.project_renderer import ProjectRenderer

logger = logging.getLogger(__name__)


class RidingOnBugs:

    logger = logging.getLogger(__name__)

    def __init__(self, renderer: ProjectRenderer):
        self._renderer: ProjectRenderer = renderer

    def render(self, output_file: str):
        logger.info('started rendering RidingOnBugs demo to ' + output_file)

        project = self.create_project()
        self._renderer.render_to_file(project, output_file)


    def create_project(self) -> Project:
        pass

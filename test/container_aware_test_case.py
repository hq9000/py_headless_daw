import logging

from py_headless_daw.application_container import ApplicationContainer


class ContainerAwareTestCase:

    _container: ApplicationContainer

    def get_container(self) -> ApplicationContainer:
        if not hasattr(self, '_container'):
            self._container: ApplicationContainer = ApplicationContainer()

        return self._container

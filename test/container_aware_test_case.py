import unittest

from py_headless_daw.application_container import ApplicationContainer


class ContainerAwareTestCase(unittest.TestCase):

    def __init__(self, method_name='runTest'):
        self._container = ApplicationContainer()
        super().__init__(method_name)

    def get_container(self) -> ApplicationContainer:
        return self._container

import logging
import unittest

from py_headless_daw.application_container import ApplicationContainer


class ContainerAwareTestCase(unittest.TestCase):

    def __init__(self, methodName='runTest'):
        self._container = ApplicationContainer()
        super().__init__(methodName)

    def get_container(self) -> ApplicationContainer:
        return self._container

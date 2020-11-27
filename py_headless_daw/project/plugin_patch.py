from py_headless_daw.project.having_parameters import HavingParameters


class PluginPatch(HavingParameters):
    def __init__(self):
        super().__init__()
        self.name: str = 'unnamed'

from py_headless_daw.project.having_parameters import HavingParameters


class PluginPreset(HavingParameters):
    def __init__(self, name: str):
        self.name: str = name
        super().__init__()

from cython_vst_loader.vst_plugin import VstPlugin as RealVstPlugin, VstHost
from py_headless_daw.project.plugins.plugin import Plugin


class VstPlugin(Plugin):
    def __init__(self, path_to_plugin: str):
        super().__init__()

        path_as_bytes: bytes = path_to_plugin.encode('utf-8')
        # this plugin instance will not be actually used for any processing
        # so it does not really matter which sample frequency and block size we assign to this
        # host
        tmp_host: VstHost = VstHost(44100, 512)
        plugin_instance: RealVstPlugin = RealVstPlugin(path_as_bytes, tmp_host)

        for i in range(0, plugin_instance.get_num_parameters()):
            name: str = plugin_instance.get_parameter_name(i)
            value: float = plugin_instance.get_parameter_value(i)
            self.add_parameter(name, value)

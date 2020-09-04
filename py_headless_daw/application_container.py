from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from py_headless_daw.compiler.project_compiler import InternalPluginProcessingStrategyFactory


class ApplicationContainer(DeclarativeContainer):

    def __init__(self):

        self.internal_plugin_processing_strategy_factory = providers.Singleton(
            InternalPluginProcessingStrategyFactory
        )
        #
        # self.project_compiler = providers.Singleton(
        #     ProjectCompiler,
        #
        # )

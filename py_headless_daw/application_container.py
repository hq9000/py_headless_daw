from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from py_headless_daw.compiler.project_compiler import InternalPluginProcessingStrategyFactory, ProjectCompiler
from py_headless_daw.project.project_renderer import ProjectRenderer
from py_headless_daw.services.wave_data_provider import WaveDataProvider


class ApplicationContainer(DeclarativeContainer):
    waveform_provider = providers.Singleton(
        WaveDataProvider
    )

    internal_plugin_processing_strategy_factory = providers.Singleton(
        InternalPluginProcessingStrategyFactory,
        waveform_provider
    )

    project_compiler = providers.Singleton(
        ProjectCompiler,
        internal_plugin_processing_strategy_factory=internal_plugin_processing_strategy_factory
    )

    project_renderer = providers.Singleton(
        ProjectRenderer,
        project_compiler=project_compiler
    )

"""The Meson generator implementation
"""

from typing import Any

from cppython_core.plugin_schema.generator import Generator, GeneratorData
from cppython_core.schema import CorePluginData, SyncData

from cppython_meson.resolution import resolve_meson_data


class MesonGenerator(Generator):
    """Meson generator"""

    def __init__(self, group_data: GeneratorData, core_data: CorePluginData) -> None:
        super().__init__(group_data, core_data)

        self._data = resolve_meson_data({}, self.core_data)

    def activate(self, data: dict[str, Any]) -> None:
        """Called when configuration data is ready

        Args:
            data: Input plugin data from pyproject.toml
        """
        self._data = resolve_meson_data(data, self.core_data)

    @staticmethod
    def name() -> str:
        """The name token

        Returns:
            Name
        """
        return "meson"

    def sync(self, results: list[SyncData]) -> None:
        """Disk sync point

        Args:
            results: Input data from providers
        """

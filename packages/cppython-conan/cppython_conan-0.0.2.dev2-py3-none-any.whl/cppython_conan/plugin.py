"""Conan provider for CPPython"""

from pathlib import Path
from typing import Any

from cppython_core.plugin_schema.provider import Provider, ProviderData
from cppython_core.schema import CorePluginData, SyncData

from cppython_conan.resolution import resolve_conan


class ConanProvider(Provider):
    """Conan provider implementation"""

    def __init__(self, group_data: ProviderData, core_data: CorePluginData) -> None:
        super().__init__(group_data, core_data)

        self.data = resolve_conan({}, self.core_data)

    @staticmethod
    def name() -> str:
        """Name token

        Returns:
            The name
        """
        return "conan"

    def activate(self, data: dict[str, Any]) -> None:
        """Called when the data is ready

        Args:
            data: The configuration data
        """

        self.data = resolve_conan(data, self.core_data)

    def sync_data(self, name: str) -> SyncData:
        """Generates Sync data

        Args:
            name: The generator name

        Returns:
            The sync data
        """

        return SyncData(name=self.name(), data=None)

    @classmethod
    async def download_tooling(cls, path: Path) -> None:
        """Downloads tooling if needed

        Args:
            path: The location to download to
        """

    def install(self) -> None:
        """Install API"""

    def supports_generator(self, name: str) -> bool:
        """Returns whether the input generator token is supported

        Args:
            name: The generator name

        Returns:
            The query result
        """

        return name == "cmake"

    def update(self) -> None:
        """Update API"""

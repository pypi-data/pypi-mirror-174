"""Conan provider for CPPython"""

from pathlib import Path
from typing import Any

from cppython_core.plugin_schema.provider import Provider
from cppython_core.schema import SyncData


class ConanProvider(Provider):
    """Conan provider implementation"""

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

"""Data resolution helpers"""

from typing import Any

from cppython_core.schema import CorePluginData

from cppython_conan.schema import ConanConfiguration, ConanData


def resolve_conan(input_data: dict[str, Any], core_date: CorePluginData) -> ConanData:
    """Resolves a table into readable data

    Args:
        input_data: The input table
        core_date: Core data

    Returns:
        The resolved data
    """

    configuration = ConanConfiguration(**input_data)

    root_directory = core_date.project_data.pyproject_file.parent

    modified_conan_file = configuration.conan_file
    if not modified_conan_file.is_absolute():
        modified_conan_file = root_directory / modified_conan_file

    return ConanData(conan_file=modified_conan_file)

"""Data definitions"""

from pathlib import Path

from cppython_core.schema import CPPythonModel
from pydantic import Field, FilePath


class ConanData(CPPythonModel):
    """_summary_"""

    conan_file: FilePath


class ConanConfiguration(CPPythonModel):
    """_summary_"""

    conan_file: Path = Field(default=Path("conanfile.py"), description="", alias="conan-file")

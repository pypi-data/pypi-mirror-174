"""Unit test the provider plugin
"""

from typing import Any

import pytest
from pytest_cppython.plugin import GeneratorUnitTests

from cppython_meson.plugin import MesonGenerator


class TestCPPythonGenerator(GeneratorUnitTests[MesonGenerator]):
    """The tests for the Meson generator"""

    @pytest.fixture(name="plugin_data", scope="session")
    def fixture_plugin_data(self) -> dict[str, Any]:
        """A required testing hook that allows data generation

        Returns:
            The constructed plugin data
        """
        return {}

    @pytest.fixture(name="plugin_type", scope="session")
    def fixture_plugin_type(self) -> type[MesonGenerator]:
        """A required testing hook that allows type generation

        Returns:
            The type of the Generator
        """
        return MesonGenerator

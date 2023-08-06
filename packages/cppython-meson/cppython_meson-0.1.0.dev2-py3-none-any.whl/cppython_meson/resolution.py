"""Builder to help resolve meson state"""

from typing import Any

from cppython_core.schema import CorePluginData

from cppython_meson.schema import MesonConfiguration, MesonData


def resolve_meson_data(data: dict[str, Any], core_data: CorePluginData) -> MesonData:
    """Resolves the input data table from defaults to requirements

    Args:
        data: The input table
        core_data: The core data to help with the resolve

    Returns:
        The resolved data
    """

    MesonConfiguration(**data)

    core_data.project_data.pyproject_file.parent.absolute()

    return MesonData()

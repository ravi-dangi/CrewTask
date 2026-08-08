"""Compat shims for Streamlit Cloud / lean Python envs."""
from __future__ import annotations

import sys
import types


def ensure_pkg_resources() -> None:
    """crewai 0.28.x telemetry imports pkg_resources (setuptools).

    Some hosts omit setuptools at runtime. Provide a minimal shim that
    supports get_distribution(name).version via importlib.metadata.
    """
    try:
        import pkg_resources  # noqa: F401
        return
    except ImportError:
        pass

    from importlib.metadata import PackageNotFoundError, version

    def get_distribution(name: str):
        class _Dist:
            def __init__(self, package_name: str) -> None:
                try:
                    self.version = version(package_name)
                except PackageNotFoundError:
                    self.version = "0.0.0"

        return _Dist(name)

    shim = types.ModuleType("pkg_resources")
    shim.get_distribution = get_distribution  # type: ignore[attr-defined]
    sys.modules["pkg_resources"] = shim

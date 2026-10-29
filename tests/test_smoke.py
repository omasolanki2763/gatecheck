"""Smoke test module for package initialization and version verification."""

from importlib.metadata import version

import gatecheck


def test_package_version_matches_metadata() -> None:
    """Verifies that gatecheck exposes a valid version matching package metadata."""
    assert gatecheck.__version__ == version("gatecheck")

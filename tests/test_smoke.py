"""Smoke test module for package initialization and version verification."""

import gatecheck


def test_package_version_is_valid() -> None:
    """Verifies that the gatecheck package imports and exposes a valid version string."""
    assert gatecheck.__version__ == "0.1.0"

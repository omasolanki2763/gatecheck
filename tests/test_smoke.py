"""Smoke test module for package initialization and version verification."""

import importlib
from importlib.metadata import PackageNotFoundError, version
from unittest.mock import patch

import gatecheck


def test_package_version_is_valid() -> None:
    """Verifies that gatecheck exposes a valid version matching package metadata."""
    expected_version = version("gatecheck")
    assert gatecheck.__version__ == expected_version
    assert len(gatecheck.__version__) > 0


def test_package_version_fallback_when_not_installed() -> None:
    """Verifies that gatecheck provides a fallback version when metadata is missing."""
    with patch("importlib.metadata.version", side_effect=PackageNotFoundError):
        reloaded = importlib.reload(gatecheck)
        assert reloaded.__version__ == "0.1.0"
    # Restore normal installed state
    importlib.reload(gatecheck)

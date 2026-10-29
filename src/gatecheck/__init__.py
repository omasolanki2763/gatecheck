"""GateCheck: Document screening and eligibility verification pipeline."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__: str = version("gatecheck")
except PackageNotFoundError:
    __version__ = "0.1.0"

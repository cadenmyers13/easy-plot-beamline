"""Unit tests for __version__.py."""

import easy_plot_beamline  # noqa


def test_package_version():
    """Ensure the package version is defined and not set to the initial
    placeholder."""
    assert hasattr(easy_plot_beamline, "__version__")
    assert easy_plot_beamline.__version__ != "0.0.0"

"""Unit tests for __version__.py."""

import easy_plot_beamline  # noqa


def test_package_version():
    """Ensure the package version is defined and not set to the initial
    placeholder."""
    actual_has_version = hasattr(easy_plot_beamline, "__version__")
    assert actual_has_version

    actual_version = easy_plot_beamline.__version__
    assert actual_version != "0.0.0"

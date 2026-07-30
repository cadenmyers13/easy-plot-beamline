import matplotlib
import numpy as np
import pytest

matplotlib.use("Agg")


def _write_xy_file(path, x, y):
    np.savetxt(path, np.column_stack([x, y]))
    return path


@pytest.fixture
def datafiles(tmp_path):
    """Write a small set of two-column data files to a temp directory.

    Returns
    -------
    dict of str to pathlib.Path
        A mapping of logical name to the written file path.
    """
    x = np.linspace(0, 10, 20)
    files = {
        "a": _write_xy_file(tmp_path / "a.gr", x, np.sin(x)),
        "b": _write_xy_file(tmp_path / "b.gr", x, 2 * np.sin(x)),
        "c": _write_xy_file(tmp_path / "c.txt", x, np.cos(x)),
    }
    files["unreadable"] = tmp_path / "unreadable.gr"
    files["unreadable"].write_text("not numeric data\nabc def\n")
    return files

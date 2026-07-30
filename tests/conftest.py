import json
from pathlib import Path

import matplotlib
import numpy as np
import pytest

matplotlib.use("Agg")


@pytest.fixture
def user_filesystem(tmp_path):
    base_dir = Path(tmp_path)
    home_dir = base_dir / "home_dir"
    home_dir.mkdir(parents=True, exist_ok=True)
    cwd_dir = base_dir / "cwd_dir"
    cwd_dir.mkdir(parents=True, exist_ok=True)

    home_config_data = {"username": "home_username", "email": "home@email.com"}
    with open(home_dir / "diffpyconfig.json", "w") as f:
        json.dump(home_config_data, f)

    yield tmp_path


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

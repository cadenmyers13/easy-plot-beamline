import argparse
from pathlib import Path

import numpy as np

from easy_plot_beamline.plotting import (
    plot_diff,
    plot_diff_matrix,
    plot_overlaid,
    plot_waterfall,
)
from easy_plot_beamline.version import __version__  # noqa


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------
def load_first_two_columns_or_skip(path: Path):
    """Try loading the first two numeric columns from a file.

    Return (x, y) arrays or None if the file cannot be parsed as numeric
    data.
    """
    try:
        data = np.loadtxt(path, usecols=(0, 1))
    except Exception:
        print(f"[warning] Skipping non-numeric or incompatible file: {path}")
        return None

    if data.ndim == 1:
        if data.size == 2:
            return data[0], data[1]
        else:
            return None

    return data[:, 0], data[:, 1]


def collect_valid_files(paths):
    """Expand directories, accept any file extension, and return only
    files that contain valid 2-column numeric data."""
    valid_files = []

    for p in map(Path, paths):
        if p.is_dir():
            for fpath in sorted(p.iterdir()):
                if fpath.is_file():
                    if load_first_two_columns_or_skip(fpath) is not None:
                        valid_files.append(fpath)

        elif p.exists() and p.is_file():
            if load_first_two_columns_or_skip(p) is not None:
                valid_files.append(p)

        else:
            print(f"[warning] Skipping missing file: {p}")

    return valid_files


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        prog="easyplot",
        description="Easily plot and visualize two-column "
        "xPDFsuite or text data.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "files",
        nargs="+",
        help="Input files or directories containing them (any extension).",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Show the program's version number and exit",
    )
    parser.add_argument(
        "--waterfall",
        action="store_true",
        help="Plot curves in a waterfall style.",
    )
    parser.add_argument(
        "--diffmatrix",
        action="store_true",
        help="Plot pairwise differences between curves.",
    )
    parser.add_argument(
        "--diff",
        action="store_true",
        help="Plot the direct difference between two curves.",
    )
    parser.add_argument(
        "--legend-right",
        action="store_true",
        help="Show legend on the right side.",
    )
    parser.add_argument(
        "--yspace",
        type=float,
        default=1.0,
        help="Vertical spacing between curves for waterfall "
        "or diffmatrix plots.",
    )

    args = parser.parse_args()

    # === version flag ===
    if args.version:
        print(f"easy-plot-beamline {__version__}")
        return

    # === Collect valid files ===
    input_files = collect_valid_files(args.files)

    if not input_files:
        print("No valid numeric data files found.")
        return

    # === Dispatch to plotting modes ===
    use_right_legend = args.legend_right

    if args.diff:
        plot_diff(input_files, legend_right=use_right_legend)

    elif args.diffmatrix:
        plot_diff_matrix(
            input_files, yspace=args.yspace, legend_right=use_right_legend
        )

    elif args.waterfall:
        plot_waterfall(
            input_files, yspace=args.yspace, legend_right=use_right_legend
        )

    else:
        plot_overlaid(input_files, legend_right=use_right_legend)


if __name__ == "__main__":
    main()

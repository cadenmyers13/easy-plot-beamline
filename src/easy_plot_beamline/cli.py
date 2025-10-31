import argparse
from pathlib import Path

from easy_plot_beamline.plotting import (
    plot_diff,
    plot_diff_matrix,
    plot_overlaid,
    plot_waterfall,
)
from easy_plot_beamline.version import __version__  # noqa


def main():
    parser = argparse.ArgumentParser(
        prog="easyplot",
        description=(
            "Easily plot and visualize two-column xPDFsuite or text data.\n\n"
            "Examples:\n"
            "  easyplot file1.gr file2.gr\n"
            "  easyplot data/ --waterfall --yspace=2\n"
            "  easyplot data/ --diffmatrix\n"
            "  easyplot file1.gr file2.gr --diff\n"
            "For more information, visit:\n"
            "https://github.com/cadenmyers13/easy-plot-beamline/"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "files",
        nargs="+",
        help="Input text or .gr files, or directories containing them.",
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
        help="Plot pairwise differences between curves (ignores inverses).",
    )
    parser.add_argument(
        "--diff",
        action="store_true",
        help="Plot the direct difference between two curves.",
    )
    parser.add_argument(
        "--yspace",
        type=float,
        default=1.0,
        help="Vertical spacing between curves for waterfall or diffmatrix plots. Use like --yspace=2",
    )

    args = parser.parse_args()

    # === version flag ===
    if args.version:
        print(f"easy-plot-beamline {__version__}")
        return

    # === Collect all input files ===
    input_files = []
    for f in args.files:
        p = Path(f)
        if p.is_dir():
            input_files.extend(sorted(p.glob("*.gr")))
            input_files.extend(sorted(p.glob("*.txt")))
        elif p.exists():
            input_files.append(p)
        else:
            print(f"[warning] Skipping missing file: {f}")

    if not input_files:
        print("No valid input files found.")
        return

    # === Dispatch behavior ===
    if args.diff:
        if len(input_files) != 2:
            print("[Error] --diff requires exactly two files.")
            return
        plot_diff(input_files)
    elif args.diffmatrix:
        plot_diff_matrix(input_files, yspace=args.yspace)
    elif args.waterfall:
        plot_waterfall(input_files, yspace=args.yspace)
    else:
        plot_overlaid(input_files)


if __name__ == "__main__":
    main()

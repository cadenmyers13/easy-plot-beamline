# cli.py
import argparse
from pathlib import Path

from plotting import Plotter


def collect_files(items):
    """Collect all files from input arguments (files or directories)."""
    collected = []
    for item in items:
        p = Path(item)
        if p.is_dir():
            for f in sorted(p.iterdir()):
                if f.is_file():
                    collected.append(f)
        elif p.is_file():
            collected.append(p)
        else:
            print(f"[warning] Skipping missing file: {item}")
    return collected


def main():
    parser = argparse.ArgumentParser(
        prog="easyplot",
        description="Easily plot and visualize two-column PDF or text data.",
    )

    parser.add_argument("files", nargs="+", help="Input files or directories.")
    parser.add_argument(
        "--version", action="store_true", help="Show version and exit"
    )
    parser.add_argument(
        "--waterfall", action="store_true", help="Waterfall plot"
    )
    parser.add_argument(
        "--diffmatrix", action="store_true", help="Pairwise difference matrix"
    )
    parser.add_argument(
        "--diff", action="store_true", help="Direct diff between two files"
    )
    parser.add_argument(
        "--yspace",
        type=float,
        default=1.0,
        help="Vertical spacing for waterfall/diffmatrix",
    )

    args = parser.parse_args()

    # Version
    if args.version:
        from easy_plot_beamline.version import __version__

        print(f"easy-plot-beamline {__version__}")
        return

    # Files
    input_files = collect_files(args.files)
    if not input_files:
        print("No valid input files found.")
        return

    plotter = Plotter()

    # Dispatch
    if args.diff:
        plotter.plot_diff(input_files)
    elif args.diffmatrix:
        plotter.plot_diff_matrix(input_files, yspace=args.yspace)
    elif args.waterfall:
        plotter.plot_waterfall(input_files, yspace=args.yspace)
    else:
        plotter.plot_overlaid(input_files)


if __name__ == "__main__":
    main()

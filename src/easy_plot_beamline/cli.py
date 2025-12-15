# cli.py
import argparse
from pathlib import Path

from easy_plot_beamline.plotting import Plotter


def collect_files(paths):
    """Accept any file extension.

    Directories are searched flat.
    """
    out = []
    for p in paths:
        P = Path(p)
        if P.is_dir():
            out.extend(sorted(P.iterdir()))
        elif P.is_file():
            out.append(P)
        else:
            print(f"[Warning] Skipping missing path: {p}")
    return out


def main():
    parser = argparse.ArgumentParser(
        prog="easyplot",
        description="Plot and visualize two-column data (any file extension).",
    )

    parser.add_argument("files", nargs="+", help="Files or directories.")

    parser.add_argument("--waterfall", action="store_true")
    parser.add_argument("--diffmatrix", action="store_true")
    parser.add_argument("--diff", action="store_true")
    parser.add_argument("--yspace", type=float, default=1.0)

    # NEW FEATURES
    parser.add_argument("--legend-right", action="store_true")
    parser.add_argument("--xmin", type=float, default=None)
    parser.add_argument("--xmax", type=float, default=None)

    args = parser.parse_args()

    files = collect_files(args.files)
    if not files:
        print("No valid files found.")
        return

    plotter = Plotter(
        legend_right=args.legend_right,
        xmin=args.xmin,
        xmax=args.xmax,
    )

    if args.diff:
        plotter.plot_diff(files)
    elif args.diffmatrix:
        plotter.plot_diff_matrix(files, yspace=args.yspace)
    elif args.waterfall:
        plotter.plot_waterfall(files, yspace=args.yspace)
    else:
        plotter.plot_overlaid(files)


if __name__ == "__main__":
    main()

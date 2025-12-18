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
            out.extend(sorted(x for x in P.iterdir() if x.is_file()))
        elif P.is_file():
            out.append(P)
        else:
            print(f"[Warning] Skipping missing path: {p}")
    return out


def parse_scale_list(scale_str, nfiles):
    """Parse --scale 4,1,2 style input."""
    if scale_str is None:
        return [1.0] * nfiles

    parts = scale_str.split(",")
    if len(parts) != nfiles:
        raise ValueError(f"--scale expects {nfiles} values, got {len(parts)}")

    return [float(p) for p in parts]


def main():
    parser = argparse.ArgumentParser(
        prog="easyplot",
        description="""
Plot and visualize two-column data (any file extension).

example usage:
--------------
# plot data overlaid
easyplot file.gr file.txt ...
# plot waterfall plot
easyplot waterfall file.gr file.txt ...
# plot difference between two datasets
easyplot diff file1.gr file2.gr
# plot difference matrix of multiple datasets
easyplot diffmatrix file1.gr file2.gr ...
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--legend-off", action="store_true", help="Disable plot legend"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    # ------------------
    # Plot overlaid
    # ------------------
    p_plot = subparsers.add_parser("plot", help="Plot data overlaid")
    p_plot.add_argument("files", nargs="+", help="Files or directories")

    # ------------------
    # Waterfall
    # ------------------
    p_waterfall = subparsers.add_parser(
        "waterfall", help="Plot waterfall plot of data"
    )
    p_waterfall.add_argument("files", nargs="+", help="Files or directories")
    p_waterfall.add_argument(
        "--yspace",
        type=float,
        default=1.0,
        help="Vertical spacing between datasets",
    )
    p_waterfall.add_argument(
        "--scale",
        help="Comma-separated scale factors per file (e.g. 4,1,0.5)",
    )
    p_waterfall.add_argument(
        "--scale-to",
        metavar="REF",
        help="Scale all datasets relative to reference file",
    )
    p_waterfall.add_argument(
        "--legend-off",
        action="store_true",
        help="Disable plot legend",
    )
    p_waterfall.add_argument("--xmin", type=float)
    p_waterfall.add_argument("--xmax", type=float)

    # ------------------
    # Diff
    # ------------------
    p_diff = subparsers.add_parser(
        "diff", help="Plot difference between two datasets"
    )
    p_diff.add_argument("files", nargs=2, help="Exactly two files")
    p_diff.add_argument("--offset", type=float, default=1.0)
    p_diff.add_argument("--xmin", type=float)
    p_diff.add_argument("--xmax", type=float)
    p_diff.add_argument(
        "--legend-off", action="store_true", help="Disable plot legend"
    )
    # ------------------
    # Diff matrix
    # ------------------
    p_diffmatrix = subparsers.add_parser(
        "diffmatrix", help="Plot permutation of differences"
    )
    p_diffmatrix.add_argument("files", nargs="+", help="Files or directories")
    p_diffmatrix.add_argument(
        "--yspace", type=float, default=1.0, help="Vertical spacing"
    )
    p_diffmatrix.add_argument("--xmin", type=float)
    p_diffmatrix.add_argument("--xmax", type=float)

    args = parser.parse_args()

    # ------------------
    # Collect files
    # ------------------
    files = collect_files(args.files)
    if not files:
        print("No valid files found.")
        return

    plotter = Plotter(
        legend_on=not args.legend_off,
        xmin=args.xmin,
        xmax=args.xmax,
    )

    # ------------------
    # Dispatch
    # ------------------
    if args.command == "waterfall":
        scales = parse_scale_list(args.scale, len(files))
        plotter.plot_waterfall(
            files,
            yspace=args.yspace,
            scales=scales,
            scale_to=args.scale_to,
        )
    elif args.command == "plot":
        plotter.plot_overlaid(files)
    elif args.command == "diff":
        plotter.plot_diff(files, offset=args.offset)
    elif args.command == "diffmatrix":
        plotter.plot_diff_matrix(files, yspace=args.yspace)


if __name__ == "__main__":
    main()

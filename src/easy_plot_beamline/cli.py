# cli.py
import argparse
from pathlib import Path

from easy_plot_beamline.plotting import Plotter


def collect_files(paths):
    """Collect data files from a mix of file and directory paths.

    Directories are searched flat (non-recursively). Any file
    extension is accepted.

    Parameters
    ----------
    paths : list of str
        The file or directory paths given on the command line.

    Returns
    -------
    list of pathlib.Path
        The files found, in sorted order within each directory.
    """
    out = []
    for p in paths:
        path = Path(p)
        if path.is_dir():
            out.extend(sorted(x for x in path.iterdir() if x.is_file()))
        elif path.is_file():
            out.append(path)
        else:
            print(f"[Warning] Skipping '{p}': no such file or directory.")
    return out


def parse_scale_list(scale_str, nfiles):
    """Parse a comma-separated `--scale` argument into scale factors.

    Parameters
    ----------
    scale_str : str or None
        The raw `--scale` value, e.g. "4,1,2". None returns a
        list of 1.0 scale factors.
    nfiles : int
        The number of files being plotted, used to validate the
        count of scale factors provided.

    Returns
    -------
    list of float
        The scale factor to apply to each file, in file order.
    """
    if scale_str is None:
        return [1.0] * nfiles

    parts = scale_str.split(",")
    if len(parts) != nfiles:
        raise ValueError(
            f"--scale expects {nfiles} comma-separated values "
            f"(one per file), but {len(parts)} were given. Please "
            "provide one scale factor for each plotted file."
        )
    return [float(p) for p in parts]


def _build_common_parser():
    """Build the parser holding options shared by every subcommand."""
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument(
        "--legend-off", action="store_true", help="Disable plot legend"
    )
    common.add_argument("--xmin", type=float, help="Lower x-axis limit")
    common.add_argument("--xmax", type=float, help="Upper x-axis limit")
    common.add_argument("--xlabel", help="X-axis label (default: no label)")
    common.add_argument("--ylabel", help="Y-axis label (default: no label)")
    common.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Save the plot to this file instead of displaying it",
    )
    return common


def main():
    common = _build_common_parser()
    parser = argparse.ArgumentParser(
        prog="easyplot",
        description=(
            "Plot and visualize two-column data (any file extension).\n\n"
            "example usage:\n"
            "--------------\n"
            "# plot data overlaid\n"
            "easyplot plot file.gr file.txt ...\n"
            "# plot waterfall plot\n"
            "easyplot waterfall file.gr file.txt ...\n"
            "# plot difference between two datasets\n"
            "easyplot diff file1.gr file2.gr\n"
            "# plot difference matrix of multiple datasets\n"
            "easyplot diffmatrix file1.gr file2.gr ..."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_plot = subparsers.add_parser(
        "plot", help="Plot data overlaid", parents=[common]
    )
    p_plot.add_argument("files", nargs="+", help="Files or directories")

    p_waterfall = subparsers.add_parser(
        "waterfall", help="Plot waterfall plot of data", parents=[common]
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

    p_diff = subparsers.add_parser(
        "diff",
        help="Plot difference between two datasets",
        parents=[common],
    )
    p_diff.add_argument("files", nargs=2, help="Exactly two files")
    p_diff.add_argument(
        "--offset",
        type=float,
        default=1.0,
        help="Vertical offset applied to the difference curve",
    )

    p_diffmatrix = subparsers.add_parser(
        "diffmatrix",
        help="Plot permutation of differences",
        parents=[common],
    )
    p_diffmatrix.add_argument("files", nargs="+", help="Files or directories")
    p_diffmatrix.add_argument(
        "--yspace", type=float, default=1.0, help="Vertical spacing"
    )

    args = parser.parse_args()

    files = collect_files(args.files)
    if not files:
        print(
            "No valid files found. Please check that the given "
            "paths point to existing files or directories."
        )
        return

    plotter = Plotter(
        legend_on=not args.legend_off,
        xmin=args.xmin,
        xmax=args.xmax,
        output=args.output,
        xlabel=args.xlabel,
        ylabel=args.ylabel,
    )

    if args.command == "plot":
        plotter.plot_overlaid(files)
    elif args.command == "waterfall":
        scales = parse_scale_list(args.scale, len(files))
        plotter.plot_waterfall(
            files,
            yspace=args.yspace,
            scales=scales,
            scale_to=args.scale_to,
        )
    elif args.command == "diff":
        plotter.plot_diff(files, offset=args.offset)
    elif args.command == "diffmatrix":
        plotter.plot_diff_matrix(files, yspace=args.yspace)


if __name__ == "__main__":
    main()

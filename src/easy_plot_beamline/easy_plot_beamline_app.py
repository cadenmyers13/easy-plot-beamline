import argparse

from easy_plot_beamline.version import __version__  # noqa


def main():
    parser = argparse.ArgumentParser(
        prog="easy-plot-beamline",
        description=(
            "Easily plot and visualize two-column data on-the-fly.\n\n"
            "For more information, visit: "
            "https://github.com/cadenmyers13/easy-plot-beamline/"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--version",
        action="store_true",
        help="Show the program's version number and exit",
    )

    args = parser.parse_args()

    if args.version:
        print(f"easy-plot-beamline {__version__}")
    else:
        # Default behavior when no arguments are given
        parser.print_help()


if __name__ == "__main__":
    main()

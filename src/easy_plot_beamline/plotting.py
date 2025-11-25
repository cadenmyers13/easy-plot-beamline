# plotting.py
import matplotlib.pyplot as plt
import numpy as np
from diffpy.utils.parsers.loaddata import loadData


class Plotter:
    """General-purpose plotter for two-column data files.

    Supports:
        - Overlaid curves
        - Direct difference
        - Difference matrix
        - Waterfall plots
    """

    def __init__(self, legend_func=None):
        self.legend_func = legend_func or plt.legend

    # ------------------------------------------------------------------
    # Data loading
    # ------------------------------------------------------------------
    def load_two_column_data(self, filepath):
        """Try diffpy.loadData → fallback to numpy.loadtxt.

        Returns (x, y) or None.
        """
        # Try diffpy
        try:
            data = loadData(filepath)
            arr = np.asarray(data)
        except Exception:
            # Try numpy
            try:
                arr = np.loadtxt(filepath)
            except Exception:
                return None

        if arr.ndim != 2 or arr.shape[1] < 2:
            return None

        return arr[:, 0], arr[:, 1]

    def load_all(self, files):
        """Load all valid two-column files and return list of (x, y,
        label)."""
        datasets = []
        for f in files:
            out = self.load_two_column_data(f)
            if out is None:
                continue
            x, y = out
            datasets.append((x, y, f.stem))
        return datasets

    # ------------------------------------------------------------------
    # Plot types
    # ------------------------------------------------------------------
    def plot_overlaid(self, files):
        """Standard overlaid plot."""
        datasets = self.load_all(files)
        if not datasets:
            print("No valid datasets to plot.")
            return

        for x, y, label in datasets:
            plt.plot(x, y, label=label)

        self.legend_func()
        plt.show()

    def plot_diff(self, files):
        """Direct difference between exactly two curves."""
        if len(files) != 2:
            print("[Error] --diff requires exactly two files.")
            return

        datasets = self.load_all(files)
        if len(datasets) != 2:
            print("Could not load both files for diff.")
            return

        x1, y1, label1 = datasets[0]
        x2, y2, label2 = datasets[1]

        if not np.allclose(x1, x2):
            print("Warning: r-grids differ. Interpolating.")
            y2 = np.interp(x1, x2, y2)

        diff = y1 - y2
        plt.plot(x1, diff, label=f"{label1} - {label2}")

        self.legend_func()
        plt.show()

    def plot_diff_matrix(self, files, yspace=1.0):
        """Pairwise differences between all curves (i < j)."""
        datasets = self.load_all(files)
        if len(datasets) < 2:
            print("Need at least 2 valid files for diffmatrix.")
            return

        for i in range(len(datasets)):
            for j in range(i + 1, len(datasets)):
                x1, y1, l1 = datasets[i]
                x2, y2, l2 = datasets[j]

                if not np.allclose(x1, x2):
                    y2 = np.interp(x1, x2, y2)
                    x = x1
                else:
                    x = x1

                diff = y1 - y2
                offset = yspace * (j - i)
                plt.plot(x, diff + offset, label=f"{l1} - {l2}")

        self.legend_func()
        plt.show()

    def plot_waterfall(self, files, yspace=1.0):
        """Offset stacked plot."""
        datasets = self.load_all(files)
        if not datasets:
            print("No valid datasets to plot.")
            return

        for i, (x, y, label) in enumerate(datasets):
            plt.plot(x, y + i * yspace, label=label)

        self.legend_func()
        plt.show()

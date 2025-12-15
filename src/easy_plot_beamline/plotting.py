# plotting.py
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from diffpy.utils.parsers.loaddata import loadData


class Plotter:
    """
    Main plotting class: handles loading data, plotting styles,
    legend placement, and x-limits.
    """

    def __init__(self, legend_right=False, xmin=None, xmax=None):
        self.legend_right = legend_right
        self.xmin = xmin
        self.xmax = xmax

    # ---------------------- Data Loading ---------------------------------

    def load_data(self, filepath: Path):
        """Try diffpy loaddata then fallback to numpy.loadtxt.

        Returns (x, y) or None on failure.
        """
        # Try diffpy
        try:
            arr = np.asarray(loadData(filepath))
            if arr.ndim == 2 and arr.shape[1] >= 2:
                return arr[:, 0], arr[:, 1]
        except Exception:
            pass

        # Try numpy
        try:
            arr = np.loadtxt(filepath)
            if arr.ndim == 2 and arr.shape[1] >= 2:
                return arr[:, 0], arr[:, 1]
        except Exception:
            pass

        return None

    # ---------------------- Legend placement ------------------------------

    def _legend(self):
        if self.legend_right:
            plt.legend(
                loc="upper left",
                bbox_to_anchor=(1.02, 1.0),
                borderaxespad=0,
                frameon=False,
            )
            plt.tight_layout(rect=[0, 0, 0.8, 1])
        else:
            plt.legend()

    # ---------------------- X-limits --------------------------------------

    def _apply_xlimits(self):
        if self.xmin is not None:
            plt.xlim(left=self.xmin)
        if self.xmax is not None:
            plt.xlim(right=self.xmax)

    # ---------------------- Plotting modes --------------------------------

    def plot_overlaid(self, files):
        plt.figure(figsize=(7, 4))

        plotted = False
        for f in files:
            data = self.load_data(f)
            if data is None:
                print(f"[Skipping] {f} (not readable)")
                continue
            x, y = data
            plt.plot(x, y, label=f.name)
            plotted = True

        if plotted:
            self._apply_xlimits()
            self._legend()
            plt.xlabel("r (Å)")
            plt.ylabel("G (Å⁻²)")
            plt.grid(True, ls="--", alpha=0.6)
            plt.show()
        else:
            print("No valid data files to plot.")

    def plot_waterfall(self, files, yspace=1.0):
        plt.figure(figsize=(7, 4))

        offset = 0
        plotted = False

        for f in files:
            data = self.load_data(f)
            if data is None:
                print(f"[Skipping] {f} (not readable)")
                continue
            x, y = data
            plt.plot(x, y + offset, label=f.name)
            offset += yspace
            plotted = True

        if plotted:
            self._apply_xlimits()
            self._legend()
            plt.xlabel("r (Å)")
            plt.ylabel("G (Å⁻²)")
            plt.grid(True, ls="--", alpha=0.6)
            plt.show()
        else:
            print("No valid data files to plot.")

    def plot_diff(self, files):
        if len(files) != 2:
            print("[Error] --diff requires exactly two files.")
            return

        d1 = self.load_data(files[0])
        d2 = self.load_data(files[1])

        if d1 is None or d2 is None:
            print("[Error] One of the two files is unreadable.")
            return

        x1, y1 = d1
        x2, y2 = d2

        if not np.allclose(x1, x2):
            y2 = np.interp(x1, x2, y2)

        plt.figure(figsize=(7, 4))
        plt.plot(x1, y1 - y2, label=f"{files[0].name} - {files[1].name}")

        self._apply_xlimits()
        self._legend()
        plt.grid(True, ls="--", alpha=0.6)
        plt.xlabel("X")
        plt.ylabel("ΔY")
        plt.show()

    def plot_diff_matrix(self, files, yspace=1.0):
        plt.figure(figsize=(7, 4))

        offset = 0
        plotted = False

        for i in range(len(files)):
            for j in range(i + 1, len(files)):

                d1 = self.load_data(files[i])
                d2 = self.load_data(files[j])

                if d1 is None or d2 is None:
                    print(f"[Skipping] {files[i].name} vs {files[j].name}")
                    continue

                x1, y1 = d1
                x2, y2 = d2

                if not np.allclose(x1, x2):
                    y2 = np.interp(x1, x2, y2)

                diff = y1 - y2

                plt.plot(
                    x1,
                    diff + offset,
                    label=f"{files[i].name} - {files[j].name}",
                    lw=1.2,
                )
                plt.axhline(offset, color="black", linewidth=0.7)
                offset += yspace
                plotted = True

        if plotted:
            self._apply_xlimits()
            self._legend()
            plt.xlabel("X")
            plt.ylabel("ΔY (multiple)")
            plt.grid(True, ls="--", alpha=0.6)
            plt.show()
        else:
            print("No valid pairwise data to compute diff matrix.")

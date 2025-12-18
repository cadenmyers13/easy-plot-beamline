# plotting.py
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from diffpy.utils.parsers.loaddata import loadData


class Plotter:
    """
    Main plotting class: handles loading data, scaling,
    plotting styles, legend placement, and x-limits.
    """

    def __init__(self, legend_on=True, xmin=None, xmax=None):
        self.legend_on = legend_on
        self.xmin = xmin
        self.xmax = xmax

    def load_data(self, filepath: Path):
        """Try diffpy loaddata then fallback to numpy.loadtxt.

        Returns (x, y) or None on failure.
        """
        try:
            arr = np.asarray(loadData(filepath))
            if arr.ndim == 2 and arr.shape[1] >= 2:
                return arr[:, 0], arr[:, 1]
        except Exception:
            pass

        try:
            arr = np.loadtxt(filepath)
            if arr.ndim == 2 and arr.shape[1] >= 2:
                return arr[:, 0], arr[:, 1]
        except Exception:
            pass

        return None

    def _apply_xlimits(self):
        if self.xmin is not None:
            plt.xlim(left=self.xmin)
        if self.xmax is not None:
            plt.xlim(right=self.xmax)

    def _legend(self):
        plt.legend(loc="upper right")

    def _set_plot_parameters(self):
        plt.xlabel("r (Å)")
        plt.ylabel("G (Å⁻²)")
        plt.grid(True)

    def _interp_to(self, x_ref, x, y):
        """Interpolate y(x) onto x_ref if needed."""
        if np.allclose(x_ref, x):
            return y
        return np.interp(x_ref, x, y)

    def _compute_scale_to_reference(self, x, y, xref, yref):
        """Compute least-squares scale factor that maps y -> yref."""
        y_interp = self._interp_to(xref, x, y)
        num = np.dot(y_interp, yref)
        den = np.dot(y_interp, y_interp)
        return 1.0 if den == 0 else num / den

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
            if self.legend_on:
                self._legend()
            self._set_plot_parameters()
            plt.show()
        else:
            print("No valid data files to plot.")

    def plot_waterfall(
        self,
        files,
        yspace=1.0,
        scales=None,
        scale_to: str | Path | None = None,
    ):
        """Waterfall plot with optional scaling.

        Parameters
        ----------
        scales : list[float] or None
            Explicit per-file scale factors.
        scale_to : Path or None
            Reference file to scale all datasets against.
        """
        plt.figure(figsize=(7, 4))

        offset = 0.0
        plotted = False
        data = []
        for f in files:
            d = self.load_data(f)
            if d is None:
                print(f"[Skipping] {f} (not readable)")
                data.append(None)
            else:
                data.append(d)

        if all(d is None for d in data):
            print("No valid data files to plot.")
            return
        nfiles = len(files)
        if scales is None:
            scales = np.ones(nfiles)
        else:
            scales = np.asarray(scales, dtype=float)
        if scale_to is not None:
            scale_to = Path(scale_to)
            if scale_to not in files:
                raise ValueError(
                    f"--scale-to reference '{scale_to}' "
                    "must be one of the plotted files"
                )
            ref_idx = files.index(scale_to)
            xref, yref = data[ref_idx]
            for i, d in enumerate(data):
                if d is None or i == ref_idx:
                    continue
                x, y = d
                s = self._compute_scale_to_reference(x, y, xref, yref)
                scales[i] *= s

        for f, d, s in zip(files, data, scales):
            if d is None:
                continue
            x, y = d
            plt.plot(x, s * y + offset, label=f.name)
            offset += yspace
            plotted = True

        if plotted:
            self._apply_xlimits()
            if self.legend_on:
                self._legend()
            self._set_plot_parameters()
            plt.show()

    def plot_diff(self, files, offset=1.0):
        if len(files) != 2:
            print("[Error] diff requires exactly two files.")
            return

        d1 = self.load_data(files[0])
        d2 = self.load_data(files[1])

        if d1 is None or d2 is None:
            print("[Error] One of the two files is unreadable.")
            return

        x1, y1 = d1
        x2, y2 = d2

        # ---------------- Determine overlapping x-range ----------------
        xmin = max(x1.min(), x2.min())
        xmax = min(x1.max(), x2.max())

        if xmin >= xmax:
            print("[Error] No overlapping x-range between datasets.")
            return
        m1 = (x1 >= xmin) & (x1 <= xmax)
        m2 = (x2 >= xmin) & (x2 <= xmax)
        x1o, y1o = x1[m1], y1[m1]
        x2o, y2o = x2[m2], y2[m2]
        y2_interp = np.interp(x1o, x2o, y2o)
        diff = y1o - y2_interp

        plt.figure(figsize=(7, 4))
        plt.plot(x1o, y1o, label=files[0].name, color="blue")
        plt.plot(x1o, y2_interp, label=files[1].name, color="red")
        plt.plot(x1o, diff - offset, label="diff", color="green")
        plt.axhline(-offset, color="black", lw=0.8)
        self._apply_xlimits()
        if self.legend_on:
            self._legend()
        self._set_plot_parameters()
        plt.show()

    def plot_diff_matrix(self, files, yspace=1.0):
        plt.figure(figsize=(7, 4))
        offset = 0.0
        plotted = False
        loaded = [(f, self.load_data(f)) for f in files]

        for i in range(len(loaded)):
            fi, d1 = loaded[i]
            if d1 is None:
                continue
            x1, y1 = d1
            for j in range(i + 1, len(loaded)):
                fj, d2 = loaded[j]
                if d2 is None:
                    continue
                x2, y2 = d2
                if not np.allclose(x1, x2):
                    y2 = np.interp(x1, x2, y2)
                diff = y1 - y2

                plt.plot(
                    x1,
                    diff + offset,
                    label=f"{fi.name} - {fj.name}",
                    lw=1.2,
                )
                plt.axhline(offset, color="black", lw=0.7)
                offset += yspace
                plotted = True

        if plotted:
            self._apply_xlimits()
            if self.legend_on:
                self._legend()
            self._set_plot_parameters()
            plt.show()
        else:
            print("No valid pairwise data to compute diff matrix.")

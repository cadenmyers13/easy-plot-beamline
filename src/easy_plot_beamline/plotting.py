# plotting.py
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from diffpy.utils.parsers.loaddata import load_data as diffpy_load_data


class Plotter:
    """Load two-column datasets and render them with matplotlib.

    Handles data loading, scaling, plotting styles, legend
    placement, and x-limits shared across all plot types.

    Parameters
    ----------
    legend_on : bool
        Whether to draw a legend on the produced plots.
    xmin : float or None
        The lower x-axis limit, or None to leave it unset.
    xmax : float or None
        The upper x-axis limit, or None to leave it unset.
    output : pathlib.Path or None
        The path to save the figure to. When None, the plot is
        shown interactively instead.
    xlabel : str or None
        The x-axis label, or None to leave the axis unlabeled.
    ylabel : str or None
        The y-axis label, or None to leave the axis unlabeled.
    """

    def __init__(
        self,
        legend_on=True,
        xmin=None,
        xmax=None,
        output=None,
        xlabel=None,
        ylabel=None,
    ):
        self.legend_on = legend_on
        self.xmin = xmin
        self.xmax = xmax
        self.output = output
        self.xlabel = xlabel
        self.ylabel = ylabel

    def load_data(self, filepath: Path):
        """Load a two-column dataset from a file.

        Try `diffpy.utils.parsers.loaddata.loadData` first, then
        fall back to `numpy.loadtxt`.

        Parameters
        ----------
        filepath : pathlib.Path
            The path to the data file.

        Returns
        -------
        tuple of numpy.ndarray or None
            The (x, y) arrays, or None if the file could not be
            parsed as two-column data.
        """
        for loader in (diffpy_load_data, np.loadtxt):
            try:
                arr = np.asarray(loader(filepath))
            except Exception:
                continue
            if arr.ndim == 2 and arr.shape[1] >= 2:
                return arr[:, 0], arr[:, 1]
        return None

    def _apply_xlimits(self):
        if self.xmin is not None:
            plt.xlim(left=self.xmin)
        if self.xmax is not None:
            plt.xlim(right=self.xmax)

    def _show_legend(self):
        plt.legend(loc="best")

    def _set_plot_parameters(self):
        if self.xlabel is not None:
            plt.xlabel(self.xlabel)
        if self.ylabel is not None:
            plt.ylabel(self.ylabel)
        plt.grid(True)

    def _new_figure(self):
        plt.figure(figsize=(7, 4))

    def _finalize_figure(self):
        """Apply shared styling and either save or show the figure."""
        self._apply_xlimits()
        if self.legend_on:
            self._show_legend()
        self._set_plot_parameters()
        if self.output is not None:
            plt.savefig(self.output)
            plt.close()
        else:
            plt.show()

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

    def _load_all(self, files):
        """Load every file, printing a warning for unreadable ones.

        Returns
        -------
        list of tuple or None
            One (x, y) entry per file, in file order, with None in
            place of any file that could not be read.
        """
        loaded = []
        for f in files:
            data = self.load_data(f)
            if data is None:
                print(f"[Skipping] {f} (not readable)")
            loaded.append(data)
        return loaded

    def plot_overlaid(self, files):
        """Plot multiple datasets overlaid on the same axes.

        Parameters
        ----------
        files : list of pathlib.Path
            The data files to plot.
        """
        data = self._load_all(files)
        if all(d is None for d in data):
            print("No valid data files to plot.")
            return

        self._new_figure()
        for f, d in zip(files, data):
            if d is None:
                continue
            x, y = d
            plt.plot(x, y, label=f.name)
        self._finalize_figure()

    def plot_waterfall(
        self,
        files,
        yspace=1.0,
        scales=None,
        scale_to: str | Path | None = None,
    ):
        """Plot datasets stacked vertically with optional scaling.

        Parameters
        ----------
        files : list of pathlib.Path
            The data files to plot.
        yspace : float
            The vertical spacing applied between successive datasets.
        scales : list of float or None
            The explicit per-file scale factors. Defaults to 1.0 for
            every file.
        scale_to : pathlib.Path or None
            A reference file to scale all datasets against, chosen
            by matching filename against `files`.
        """
        data = self._load_all(files)
        if all(d is None for d in data):
            print("No valid data files to plot.")
            return

        nfiles = len(files)
        scales = (
            np.ones(nfiles)
            if scales is None
            else np.asarray(scales, dtype=float)
        )

        if scale_to is not None:
            ref_idx = self._find_reference_index(files, scale_to)
            xref, yref = data[ref_idx]
            for i, d in enumerate(data):
                if d is None or i == ref_idx:
                    continue
                x, y = d
                scales[i] *= self._compute_scale_to_reference(x, y, xref, yref)

        self._new_figure()
        offset = 0.0
        for f, d, s in zip(files, data, scales):
            if d is None:
                continue
            x, y = d
            plt.plot(x, s * y + offset, label=f.name)
            offset += yspace
        self._finalize_figure()

    def _find_reference_index(self, files, scale_to):
        """Find the index of the file matching the --scale-to name.

        Parameters
        ----------
        files : list of pathlib.Path
            The plotted files.
        scale_to : str or pathlib.Path
            The filename of the reference file.

        Returns
        -------
        int
            The index of the matching file in `files`.
        """
        target_name = Path(scale_to).name
        for i, f in enumerate(files):
            if f.name == target_name:
                return i
        raise ValueError(
            f"--scale-to reference '{scale_to}' does not match any "
            "of the plotted files. Please pass the filename of one "
            "of the files being plotted."
        )

    def plot_diff(self, files, offset=1.0):
        """Plot two datasets along with their interpolated difference.

        Parameters
        ----------
        files : list of pathlib.Path
            Exactly two data files to compare.
        offset : float
            The vertical offset applied to the difference curve.
        """
        if len(files) != 2:
            print(
                "[Error] diff requires exactly two files. Please "
                "pass exactly two file paths."
            )
            return

        d1 = self.load_data(files[0])
        d2 = self.load_data(files[1])
        if d1 is None or d2 is None:
            print(
                "[Error] One of the two files could not be read. "
                "Please check that both files contain two-column data."
            )
            return

        x1, y1 = d1
        x2, y2 = d2

        xmin = max(x1.min(), x2.min())
        xmax = min(x1.max(), x2.max())
        if xmin >= xmax:
            print(
                "[Error] The two datasets do not share an overlapping "
                "x-range, so no difference can be computed."
            )
            return

        m1 = (x1 >= xmin) & (x1 <= xmax)
        m2 = (x2 >= xmin) & (x2 <= xmax)
        x1o, y1o = x1[m1], y1[m1]
        x2o, y2o = x2[m2], y2[m2]
        y2_interp = np.interp(x1o, x2o, y2o)
        diff = y1o - y2_interp

        self._new_figure()
        plt.plot(x1o, y1o, label=files[0].name, color="blue")
        plt.plot(x1o, y2_interp, label=files[1].name, color="red")
        plt.plot(x1o, diff - offset, label="diff", color="green")
        plt.axhline(-offset, color="black", lw=0.8)
        self._finalize_figure()

    def plot_diff_matrix(self, files, yspace=1.0):
        """Plot the pairwise differences between every pair of datasets.

        Parameters
        ----------
        files : list of pathlib.Path
            The data files to compare pairwise.
        yspace : float
            The vertical spacing applied between successive
            difference curves.
        """
        data = self._load_all(files)
        if all(d is None for d in data):
            print("No valid pairwise data to compute diff matrix.")
            return

        self._new_figure()
        offset = 0.0
        plotted = False
        for i in range(len(files)):
            d1 = data[i]
            if d1 is None:
                continue
            x1, y1 = d1
            for j in range(i + 1, len(files)):
                d2 = data[j]
                if d2 is None:
                    continue
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
                plt.axhline(offset, color="black", lw=0.7)
                offset += yspace
                plotted = True

        if plotted:
            self._finalize_figure()
        else:
            plt.close()
            print("No valid pairwise data to compute diff matrix.")

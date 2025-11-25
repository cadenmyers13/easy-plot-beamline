from __future__ import annotations

import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


# ---------------------------------------------------------------------------
# Data Loading Helpers
# ---------------------------------------------------------------------------
def _load_data(filepath: Path):
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    lines = filepath.read_text().splitlines()
    label_line = None
    data_start = None

    # Find #L label and first numeric line
    for i, line in enumerate(lines):
        stripped = line.strip()

        if stripped.startswith("#L"):
            label_line = stripped[2:].strip()
            continue

        if label_line is not None:
            parts = re.split(r"[,\s]+", stripped)
            try:
                [float(p) for p in parts]
                data_start = i
                break
            except ValueError:
                continue

    if label_line is None or data_start is None:
        raise ValueError(
            f"{filepath}: could not find #L labels or numeric data"
        )

    # Parse labels
    parts = re.split(r"[,\s]+", label_line)
    xlabel = parts[0] if len(parts) >= 1 else "X"
    ylabel = parts[1] if len(parts) >= 2 else "Y"

    # Clean labels
    for sym, repl in [
        ("($\\AA$)", "(Å)"),
        ("($\\AA^{-1}$)", "(Å⁻¹)"),
        ("($\\AA^{-2}$)", "(Å⁻²)"),
        ("($\\AA^{-3}$)", "(Å⁻³)"),
    ]:
        xlabel = xlabel.replace(sym, repl)
        ylabel = ylabel.replace(sym, repl)

    # Numeric data
    try:
        data = np.loadtxt(lines[data_start:])
    except Exception as e:
        raise ValueError(f"{filepath}: could not parse numeric data: {e}")

    if data.ndim == 1 or data.shape[1] < 2:
        raise ValueError(f"{filepath}: expected at least two numeric columns")

    return data[:, 0], data[:, 1], xlabel, ylabel


# ---------------------------------------------------------------------------
# Plotter Class
# ---------------------------------------------------------------------------
class Plotter:
    def __init__(self, legend_right: bool = False):
        """
        Parameters
        ----------
        legend_right : bool
            If True, place the legend outside the plot on the right.
        """
        self.legend_right = legend_right

    # ---------------------------
    # Internal utility methods
    # ---------------------------
    def _configure_plot(self, xlabel: str, ylabel: str):
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(True, ls="--", alpha=0.6)

    def _show_legend(self):
        """Default legend: inside plot."""
        plt.legend()

    def _show_legend_right(self):
        """Legend on right side."""
        plt.legend(
            loc="upper left",
            bbox_to_anchor=(1.02, 1.0),
            borderaxespad=0,
            frameon=False,
        )
        plt.tight_layout(rect=[0, 0, 0.8, 1])

    def _maybe_show_legend(self):
        if self.legend_right:
            self._show_legend_right()
        else:
            self._show_legend()

    # ---------------------------
    # Public plotting functions
    # ---------------------------
    def plot_overlaid(self, files: list[Path]):
        plt.figure(figsize=(7, 4))
        xlabel, ylabel = "X", "Y"

        for f in files:
            try:
                x, y, xlabel, ylabel = _load_data(f)
                plt.plot(x, y, label=f.name, lw=1.5)
            except Exception as e:
                print(f"[Error] {f}: {e}")
                continue

        self._configure_plot(xlabel, ylabel)
        self._maybe_show_legend()
        plt.show()

    def plot_waterfall(self, files: list[Path], yspace: float = 1.0):
        plt.figure(figsize=(7, 4))
        xlabel, ylabel = "X", "Y"

        for i, f in enumerate(files):
            try:
                x, y, xlabel, ylabel = _load_data(f)
                plt.plot(x, y + i * yspace, label=f.name, lw=1.5)
            except Exception as e:
                print(f"[Error] {f}: {e}")
                continue

        self._configure_plot(xlabel, ylabel)
        self._maybe_show_legend()
        plt.show()

    def plot_diff_matrix(self, files: list[Path], yspace: float = 1.0):
        plt.figure(figsize=(7, 4))
        xlabel, ylabel = "X", "Y"
        offset = 0.0

        for i in range(len(files)):
            for j in range(i + 1, len(files)):
                try:
                    x1, y1, xlabel, ylabel = _load_data(files[i])
                    x2, y2, _, _ = _load_data(files[j])

                    if not np.allclose(x1, x2):
                        y2 = np.interp(x1, x2, y2)

                    diff = y1 - y2

                    plt.plot(
                        x1,
                        diff + offset,
                        label=f"{files[i].name} - {files[j].name}",
                        lw=1.3,
                    )
                    plt.axhline(offset, color="black", linewidth=0.8)

                    offset += yspace

                except Exception as e:
                    print(f"[Error] {files[i]} vs {files[j]}: {e}")
                    continue

        self._configure_plot(xlabel, f"Δ{ylabel}")
        self._maybe_show_legend()
        plt.show()

    def plot_diff(self, files: list[Path]):
        if len(files) != 2:
            print("[Error] --diff requires exactly two files.")
            return

        try:
            x1, y1, xlabel, ylabel = _load_data(files[0])
            x2, y2, _, _ = _load_data(files[1])

            if not np.allclose(x1, x2):
                y2 = np.interp(x1, x2, y2)

            diff = y1 - y2

            plt.figure(figsize=(7, 4))
            plt.plot(
                x1, diff, label=f"{files[0].name} - {files[1].name}", lw=1.6
            )

            self._configure_plot(xlabel, f"Δ{ylabel}")
            self._maybe_show_legend()
            plt.show()

        except Exception as e:
            print(f"[Error] {e}")

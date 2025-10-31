from __future__ import annotations
import re
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def _load_data(filepath: Path):
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    lines = filepath.read_text().splitlines()
    label_line = None
    data_start = None
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("#L"):
            label_line = stripped[2:].strip()
        elif label_line is not None:
            parts = re.split(r"[,\s]+", stripped)
            try:
                [float(p) for p in parts]
                data_start = i
                break
            except ValueError:
                continue
    if label_line is None or data_start is None:
        raise ValueError(f"{filepath}: could not find #L labels or numeric data")
    parts = re.split(r"[,\s]+", label_line)
    xlabel = parts[0] if len(parts) >= 1 else "X"
    ylabel = parts[1] if len(parts) >= 2 else "Y"
    xlabel = xlabel.replace("($\\AA$)", "(Å)").replace("($\\AA^{-1}$)", "(Å⁻¹)").replace("($\\AA^{-2}$)", "(Å⁻²)")
    ylabel = ylabel.replace("($\\AA$)", "(Å)").replace("($\\AA^{-1}$)", "(Å⁻¹)").replace("($\\AA^{-2}$)", "(Å⁻²)")
    try:
        data = np.loadtxt(lines[data_start:])
    except Exception as e:
        raise ValueError(f"{filepath}: could not parse numeric data: {e}")
    if data.ndim == 1 or data.shape[1] < 2:
        raise ValueError(f"{filepath}: expected at least two numeric columns")
    return data[:, 0], data[:, 1], xlabel, ylabel

def _parse_labels(line: str | None):
    if not line:
        return "X", "Y"
    parts = re.split(r"[,\s]+", line.strip())
    if len(parts) < 2:
        return "X", "Y"
    def _clean(lbl: str) -> str:
        lbl = (
            lbl.replace("($\\AA$)", "(Å)")
            .replace("($\\AA^{-1}$)", "(Å⁻¹)")
            .replace("($\\AA^{-2}$)", "(Å⁻²)")
            .replace("($\\AA^{-3}$)", "(Å⁻³)")
        )
        return lbl.strip()
    return _clean(parts[0]), _clean(parts[1])

def _configure_plot(xlabel: str, ylabel: str):
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True, ls="--", alpha=0.6)

def _show_legend_right():
    plt.legend(
        loc="upper left",
        bbox_to_anchor=(1.02, 1.0),
        borderaxespad=0,
        frameon=False,
    )
    plt.tight_layout(rect=[0, 0, 0.8, 1])

def plot_overlaid(files: list[Path]):
    plt.figure(figsize=(7, 4))
    xlabel, ylabel = "X", "Y"
    for f in files:
        try:
            x, y, xlabel, ylabel = _load_data(f)
            plt.plot(x, y, label=f.name, lw=1.5)
        except Exception as e:
            print(f"[Error] {f}: {e}")
            continue
    _configure_plot(xlabel, ylabel)
    _show_legend_right()
    plt.show()

def plot_waterfall(files: list[Path], yspace: float = 1.0):
    plt.figure(figsize=(7, 4))
    xlabel, ylabel = "X", "Y"
    for i, f in enumerate(files):
        try:
            x, y, xlabel, ylabel = _load_data(f)
            plt.plot(x, y + i * yspace, label=f.name, lw=1.5)
        except Exception as e:
            print(f"[Error] {f}: {e}")
            continue
    _configure_plot(xlabel, ylabel)
    _show_legend_right()
    plt.show()

def plot_diff_matrix(files: list[Path], yspace: float = 1.0):
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
                plt.plot(x1, diff + offset, label=f"{files[i].name} - {files[j].name}", lw=1.3)
                plt.axhline(offset, color="black", linewidth=0.8)
                offset += yspace
            except Exception as e:
                print(f"[Error] {files[i]} vs {files[j]}: {e}")
                continue
    _configure_plot(xlabel, f"Δ{ylabel}")
    _show_legend_right()
    plt.show()

def plot_diff(files: list[Path]):
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
        plt.plot(x1, diff, lw=1.5, label=f"{files[0].name} - {files[1].name}")
        plt.axhline(0, color="black", linewidth=0.8)
        _configure_plot(xlabel, f"Δ{ylabel}")
        _show_legend_right()
        plt.show()
    except Exception as e:
        print(f"[Error] {e}")

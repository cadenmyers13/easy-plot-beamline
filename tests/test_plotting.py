"""Unit tests for the Plotter class in plotting.py."""

import matplotlib.pyplot as plt
import numpy as np
import pytest

from easy_plot_beamline.plotting import Plotter


class TestLoadData:
    # C1: two-column whitespace-delimited file, expect parsed x, y arrays
    # C2: unreadable/non-numeric file, expect None
    @pytest.mark.parametrize(
        "key, expected_none",
        [
            ("a", False),
            ("unreadable", True),
        ],
    )
    def test_load_data(self, datafiles, key, expected_none):
        plotter = Plotter()
        result = plotter.load_data(datafiles[key])
        if expected_none:
            assert result is None
        else:
            x, y = result
            assert len(x) == len(y) == 20


class TestFindReferenceIndex:
    # C1: scale-to name matches a plotted file, expect its index
    # C2: scale-to name matches nothing, expect ValueError
    def test_match_found(self, datafiles):
        plotter = Plotter()
        files = [datafiles["a"], datafiles["b"]]
        assert plotter._find_reference_index(files, "b.gr") == 1

    def test_match_by_full_path_also_works(self, datafiles):
        plotter = Plotter()
        files = [datafiles["a"], datafiles["b"]]
        assert plotter._find_reference_index(files, datafiles["b"]) == 1

    def test_no_match_raises(self, datafiles):
        plotter = Plotter()
        files = [datafiles["a"], datafiles["b"]]
        with pytest.raises(ValueError, match="does not match any"):
            plotter._find_reference_index(files, "missing.gr")


class TestComputeScaleToReference:
    def test_recovers_known_scale_factor(self):
        plotter = Plotter()
        x = np.linspace(0, 10, 50)
        y = np.sin(x)
        yref = 3.0 * y
        scale = plotter._compute_scale_to_reference(x, y, x, yref)
        assert scale == pytest.approx(3.0)

    def test_zero_data_returns_one(self):
        plotter = Plotter()
        x = np.linspace(0, 10, 5)
        y = np.zeros_like(x)
        scale = plotter._compute_scale_to_reference(x, y, x, y)
        assert scale == 1.0


class TestSetPlotParameters:
    # C1: no labels given, expect axes left unlabeled
    # C2: labels given, expect axes labeled with the provided text
    def test_no_labels_by_default(self):
        plt.figure()
        Plotter()._set_plot_parameters()
        ax = plt.gca()
        assert ax.get_xlabel() == ""
        assert ax.get_ylabel() == ""
        plt.close()

    def test_custom_labels_are_applied(self):
        plt.figure()
        plotter = Plotter(xlabel="r (Å)", ylabel="G (Å⁻²)")
        plotter._set_plot_parameters()
        ax = plt.gca()
        assert ax.get_xlabel() == "r (Å)"
        assert ax.get_ylabel() == "G (Å⁻²)"
        plt.close()


class TestPlotOverlaid:
    # C1: all files readable, expect a saved figure
    # C2: no files readable, expect no figure written and a message printed
    def test_all_readable_saves_figure(self, datafiles, tmp_path, capsys):
        output = tmp_path / "out.png"
        plotter = Plotter(output=output)
        plotter.plot_overlaid([datafiles["a"], datafiles["b"]])
        assert output.exists()

    def test_no_readable_files_prints_message(
        self, datafiles, tmp_path, capsys
    ):
        output = tmp_path / "out.png"
        plotter = Plotter(output=output)
        plotter.plot_overlaid([datafiles["unreadable"]])
        assert not output.exists()
        assert "No valid data files to plot." in capsys.readouterr().out

    def test_partial_readable_skips_bad_file(
        self, datafiles, tmp_path, capsys
    ):
        output = tmp_path / "out.png"
        plotter = Plotter(output=output)
        plotter.plot_overlaid([datafiles["a"], datafiles["unreadable"]])
        assert output.exists()
        assert "[Skipping]" in capsys.readouterr().out


class TestPlotWaterfall:
    def test_saves_figure_with_default_scales(self, datafiles, tmp_path):
        output = tmp_path / "out.png"
        plotter = Plotter(output=output)
        plotter.plot_waterfall([datafiles["a"], datafiles["b"]])
        assert output.exists()

    def test_scale_to_matches_by_filename(self, datafiles, tmp_path):
        output = tmp_path / "out.png"
        plotter = Plotter(output=output)
        plotter.plot_waterfall(
            [datafiles["a"], datafiles["b"]],
            scale_to="a.gr",
        )
        assert output.exists()

    def test_scale_to_unknown_reference_raises(self, datafiles, tmp_path):
        plotter = Plotter(output=tmp_path / "out.png")
        with pytest.raises(ValueError, match="does not match any"):
            plotter.plot_waterfall(
                [datafiles["a"], datafiles["b"]],
                scale_to="missing.gr",
            )


class TestPlotDiff:
    # C1: two readable, overlapping files, expect a saved figure
    # C2: wrong number of files, expect an error message and no figure
    # C3: an unreadable file, expect an error message and no figure
    def test_two_valid_files_saves_figure(self, datafiles, tmp_path):
        output = tmp_path / "out.png"
        plotter = Plotter(output=output)
        plotter.plot_diff([datafiles["a"], datafiles["b"]])
        assert output.exists()

    def test_wrong_file_count_prints_error(self, datafiles, tmp_path, capsys):
        output = tmp_path / "out.png"
        plotter = Plotter(output=output)
        plotter.plot_diff([datafiles["a"]])
        assert not output.exists()
        assert "exactly two files" in capsys.readouterr().out

    def test_unreadable_file_prints_error(self, datafiles, tmp_path, capsys):
        output = tmp_path / "out.png"
        plotter = Plotter(output=output)
        plotter.plot_diff([datafiles["a"], datafiles["unreadable"]])
        assert not output.exists()
        assert "could not be read" in capsys.readouterr().out

    def test_non_overlapping_x_range_prints_error(self, tmp_path, capsys):
        x1 = np.linspace(0, 1, 10)
        x2 = np.linspace(5, 6, 10)
        f1 = tmp_path / "f1.gr"
        f2 = tmp_path / "f2.gr"
        np.savetxt(f1, np.column_stack([x1, x1]))
        np.savetxt(f2, np.column_stack([x2, x2]))

        output = tmp_path / "out.png"
        plotter = Plotter(output=output)
        plotter.plot_diff([f1, f2])
        assert not output.exists()
        assert "overlapping x-range" in capsys.readouterr().out


class TestPlotDiffMatrix:
    def test_multiple_files_saves_figure(self, datafiles, tmp_path):
        output = tmp_path / "out.png"
        plotter = Plotter(output=output)
        plotter.plot_diff_matrix(
            [datafiles["a"], datafiles["b"], datafiles["c"]]
        )
        assert output.exists()

    def test_single_file_prints_message(self, datafiles, tmp_path, capsys):
        output = tmp_path / "out.png"
        plotter = Plotter(output=output)
        plotter.plot_diff_matrix([datafiles["a"]])
        assert not output.exists()
        assert "diff matrix" in capsys.readouterr().out

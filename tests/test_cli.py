"""Unit tests for the easyplot command-line interface in cli.py."""

import pytest

from easy_plot_beamline.cli import collect_files, main, parse_scale_list


class TestCollectFiles:
    # C1: mix of files and directories, expect all files flattened
    # C2: missing path, expect it skipped with a warning
    def test_files_and_directories_are_flattened(self, datafiles, tmp_path):
        subdir = tmp_path / "sub"
        subdir.mkdir()
        nested = subdir / "nested.gr"
        nested.write_text("0 0\n1 1\n")

        files = collect_files([str(datafiles["a"]), str(subdir)])

        assert datafiles["a"] in files
        assert nested in files

    def test_missing_path_is_skipped(self, tmp_path, capsys):
        missing = tmp_path / "does_not_exist.gr"
        files = collect_files([str(missing)])
        assert files == []
        assert "no such file or directory" in capsys.readouterr().out


class TestParseScaleList:
    # C1: no --scale given, expect a list of 1.0
    # C2: matching count, expect parsed floats
    # C3: mismatched count, expect ValueError
    def test_none_returns_default_scales(self):
        expected_scales = [1.0, 1.0, 1.0]
        assert parse_scale_list(None, 3) == expected_scales

    def test_parses_matching_count(self):
        expected_scales = [4.0, 1.0, 0.5]
        assert parse_scale_list("4,1,0.5", 3) == expected_scales

    def test_mismatched_count_raises(self):
        with pytest.raises(ValueError, match="expects 3"):
            parse_scale_list("1,2", 3)


class TestMainDispatch:
    # C1: plot command with no explicit --xmin/--xmax, expect no crash
    # C2: each subcommand accepts --legend-off after the subcommand name
    @pytest.mark.parametrize("command", ["plot", "waterfall", "diffmatrix"])
    def test_multi_file_commands_run(
        self, datafiles, tmp_path, monkeypatch, command
    ):
        output = tmp_path / "out.png"
        monkeypatch.setattr(
            "sys.argv",
            [
                "easyplot",
                command,
                str(datafiles["a"]),
                str(datafiles["b"]),
                "--legend-off",
                "-o",
                str(output),
            ],
        )
        main()
        assert output.exists()

    def test_diff_command_runs(self, datafiles, tmp_path, monkeypatch):
        output = tmp_path / "out.png"
        monkeypatch.setattr(
            "sys.argv",
            [
                "easyplot",
                "diff",
                str(datafiles["a"]),
                str(datafiles["b"]),
                "--legend-off",
                "-o",
                str(output),
            ],
        )
        main()
        assert output.exists()

    def test_no_valid_files_prints_message(
        self, tmp_path, monkeypatch, capsys
    ):
        missing = tmp_path / "missing.gr"
        monkeypatch.setattr("sys.argv", ["easyplot", "plot", str(missing)])
        main()
        assert "No valid files found." in capsys.readouterr().out

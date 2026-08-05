=============
Release notes
=============

.. current developments

0.2.0
=====

**Added:**

* Add ``-o/--output`` option to save plots to a file instead of displaying them interactively.
* Add ``--xlabel``/``--ylabel`` options to set axis labels; axes are left unlabeled by default.
* Add unit tests for the CLI and plotting modules.
* Add argument ``--legend-right`` which shows the legend on the right side.
* Add support for Python 3.14.

**Changed:**

* Match ``--scale-to`` against the plotted files by filename instead of exact path.
* Axes are no longer labeled "r (Å)" / "G (Å⁻²)" by default; pass ``--xlabel``/``--ylabel`` explicitly if labels are wanted.

**Fixed:**

* Fix ``easyplot plot ...`` crashing because ``--xmin``/ ``--xmax`` were not defined on that subcommand.
* Fix the top-level ``--legend-off`` flag being silently overwritten by the ``waterfall``/ ``diff`` subcommands' own defaults.

:tocdepth: -1

.. index:: getting-started

.. _getting-started:

================
Getting started
================

``easy-plot-beamline`` provides the ``easyplot`` command-line tool for quickly
plotting two-column data without writing a plotting script. It is intended for
on-the-fly visualization at the beamline, where you want to look at a file, or a
directory of files, as soon as it is written.

Installation
------------

Install the latest release from PyPI::

    pip install easy-plot-beamline

Confirm that the installation succeeded::

    python -c "import easy_plot_beamline; print(easy_plot_beamline.__version__)"

    easyplot -h

Input data
----------

Every command reads two-column numerical data. The first column is used as the
x values and the second as the y values. Files are loaded with
``diffpy.utils.parsers.loaddata.loadData``, falling back to ``numpy.loadtxt``,
so comment headers written by common beamline software are handled
automatically.

The file extension is not inspected, so ``.gr``, ``.chi``, ``.txt``, ``.dat``,
and extensionless files all work. Files with more than two columns are accepted
and the extra columns are ignored.

Any file that cannot be parsed as two-column data is reported and skipped rather
than aborting the plot.

Passing files and directories
-----------------------------

Every command accepts any mix of file and directory paths. A directory is
searched flat, meaning its files are included but its subdirectories are not,
and the files within it are sorted by name:

.. code-block:: bash

    # Three explicit files
    easyplot plot scan01.gr scan02.gr scan03.gr

    # Every file in a directory, sorted by name
    easyplot plot ./reduced_data/

    # A directory plus one extra file
    easyplot plot ./reduced_data/ reference.gr

Legend entries use the filename only, not the full path.

Commands
--------

``easyplot`` has four subcommands. Each accepts ``-h`` to show its own options:

.. code-block:: bash

    easyplot plot -h
    easyplot waterfall -h
    easyplot diff -h
    easyplot diffmatrix -h

Overlay datasets with ``plot``
""""""""""""""""""""""""""""""

``plot`` draws every dataset on the same axes, which is the fastest way to
compare datasets that share a y scale:

.. code-block:: bash

    easyplot plot scan01.gr scan02.gr scan03.gr

.. _waterfall:

Stack datasets with ``waterfall``
"""""""""""""""""""""""""""""""""

``waterfall`` offsets each successive dataset vertically so that curves which
would otherwise sit on top of one another can be read individually:

.. code-block:: bash

    easyplot waterfall ./reduced_data/

Use ``--yspace`` to control the vertical spacing between datasets. Larger values
spread the curves further apart:

.. code-block:: bash

    easyplot waterfall ./reduced_data/ --yspace 2.5

Datasets collected with different counting times often need to be put on a
common scale before stacking. There are two ways to do this.

Use ``--scale`` to set the scale factor for each file explicitly. It takes one
comma-separated value per file, in the order the files are plotted:

.. code-block:: bash

    easyplot waterfall scan01.gr scan02.gr scan03.gr --scale 4,1,0.5

Use ``--scale-to`` to let ``easyplot`` compute the factors for you. Give it the
name of one of the files being plotted, and every other dataset is scaled onto
that reference by a least-squares fit:

.. code-block:: bash

    easyplot waterfall scan01.gr scan02.gr scan03.gr --scale-to scan02.gr

``--scale-to`` is matched against the plotted files by filename, so
``scan02.gr`` and ``./reduced_data/scan02.gr`` both select the same file. The
reference dataset itself is left unscaled. Datasets that do not share an x grid
with the reference are interpolated onto it before the factor is computed.

``--scale`` and ``--scale-to`` can be combined, in which case the explicit
factor is applied on top of the fitted one.

Compare two datasets with ``diff``
""""""""""""""""""""""""""""""""""

``diff`` takes exactly two files and plots both datasets together with their
difference curve below:

.. code-block:: bash

    easyplot diff scan01.gr scan02.gr

The two datasets are trimmed to their overlapping x range and the second is
interpolated onto the x grid of the first, so files sampled on different grids
can be compared directly. If the two files share no overlapping x range, the
command reports this and exits without plotting.

The difference curve is drawn below the data, separated by ``--offset``:

.. code-block:: bash

    easyplot diff scan01.gr scan02.gr --offset 3.0

Compare many datasets with ``diffmatrix``
"""""""""""""""""""""""""""""""""""""""""

``diffmatrix`` plots the difference between every pair of datasets, stacked
vertically. This is useful for spotting which dataset in a series is the odd one
out:

.. code-block:: bash

    easyplot diffmatrix ./reduced_data/ --yspace 2.0

Note that the number of curves grows quickly with the number of files, since a
set of *n* files produces *n(n-1)/2* difference curves. Ten files already give
45 curves.

Shared options
--------------

The following options are accepted by all four subcommands.

.. list-table::
   :widths: 20 80
   :header-rows: 1

   * - Option
     - Description
   * - ``--xmin``
     - Set the lower x-axis limit.
   * - ``--xmax``
     - Set the upper x-axis limit.
   * - ``--xlabel``
     - Set the x-axis label. Axes are unlabeled by default.
   * - ``--ylabel``
     - Set the y-axis label. Axes are unlabeled by default.
   * - ``--legend-off``
     - Do not draw a legend.
   * - ``-o``, ``--output``
     - Save the figure to this path instead of displaying it.

For example, to restrict the plotted range and label the axes for PDF data:

.. code-block:: bash

    easyplot plot ./reduced_data/ --xmin 1.5 --xmax 20 \
        --xlabel "r (Å)" --ylabel "G (Å$^{-2}$)"

Saving instead of displaying
----------------------------

Without ``-o``, ``easyplot`` opens an interactive matplotlib window and blocks
until you close it. Passing ``-o`` writes the figure to a file and returns
immediately, which is what you want when scripting or working over SSH without
display forwarding:

.. code-block:: bash

    easyplot waterfall ./reduced_data/ -o waterfall.png

The output format is chosen by matplotlib from the file extension, so ``.png``,
``.pdf``, and ``.svg`` all work.

Using the API directly
----------------------

Everything the CLI does is available from the :class:`~easy_plot_beamline.plotting.Plotter`
class, which is useful when you want to drive plotting from a script or
notebook:

.. code-block:: python

    from pathlib import Path

    from easy_plot_beamline.plotting import Plotter

    files = sorted(Path("reduced_data").glob("*.gr"))

    plotter = Plotter(xmin=1.5, xmax=20, xlabel="r (Å)", ylabel="G (Å$^{-2}$)")
    plotter.plot_waterfall(files, yspace=2.0, scale_to="scan02.gr")

See the :doc:`Package API <api/easy_plot_beamline>` for the full set of
parameters and methods.

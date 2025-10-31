|Icon| |title|_
===============

.. |title| replace:: easy-plot-beamline
.. _title: https://cadenmyers13.github.io/easy-plot-beamline

.. |Icon| image:: https://avatars.githubusercontent.com/cadenmyers13
        :target: https://cadenmyers13.github.io/easy-plot-beamline
        :height: 100px

|PyPI| |Forge| |PythonVersion| |PR|

|CI| |Codecov| |Black| |Tracking|

.. |Black| image:: https://img.shields.io/badge/code_style-black-black
        :target: https://github.com/psf/black

.. |CI| image:: https://github.com/cadenmyers13/easy-plot-beamline/actions/workflows/matrix-and-codecov-on-merge-to-main.yml/badge.svg
        :target: https://github.com/cadenmyers13/easy-plot-beamline/actions/workflows/matrix-and-codecov-on-merge-to-main.yml

.. |Codecov| image:: https://codecov.io/gh/cadenmyers13/easy-plot-beamline/branch/main/graph/badge.svg
        :target: https://codecov.io/gh/cadenmyers13/easy-plot-beamline

.. |Forge| image:: https://img.shields.io/conda/vn/conda-forge/easy-plot-beamline
        :target: https://anaconda.org/conda-forge/easy-plot-beamline

.. |PR| image:: https://img.shields.io/badge/PR-Welcome-29ab47ff
        :target: https://github.com/cadenmyers13/easy-plot-beamline/pulls

.. |PyPI| image:: https://img.shields.io/pypi/v/easy-plot-beamline
        :target: https://pypi.org/project/easy-plot-beamline/

.. |PythonVersion| image:: https://img.shields.io/pypi/pyversions/easy-plot-beamline
        :target: https://pypi.org/project/easy-plot-beamline/

.. |Tracking| image:: https://img.shields.io/badge/issue_tracking-github-blue
        :target: https://github.com/cadenmyers13/easy-plot-beamline/issues

Easily plot and visualize two-column data on-the-fly.

* LONGER DESCRIPTION HERE

For more information about the easy-plot-beamline library, please consult our `online documentation <https://cadenmyers13.github.io/easy-plot-beamline>`_.

Citation
--------

If you use easy-plot-beamline in a scientific publication, we would like you to cite this package as

        easy-plot-beamline Package, https://github.com/cadenmyers13/easy-plot-beamline

Installation
------------

The preferred method is to use `Miniconda Python
<https://docs.conda.io/projects/miniconda/en/latest/miniconda-install.html>`_
and install from the "conda-forge" channel of Conda packages.

To add "conda-forge" to the conda channels, run the following in a terminal. ::

        conda config --add channels conda-forge

We want to install our packages in a suitable conda environment.
The following creates and activates a new environment named ``easy-plot-beamline_env`` ::

        conda create -n easy-plot-beamline_env easy-plot-beamline
        conda activate easy-plot-beamline_env

The output should print the latest version displayed on the badges above.

If the above does not work, you can use ``pip`` to download and install the latest release from
`Python Package Index <https://pypi.python.org>`_.
To install using ``pip`` into your ``easy-plot-beamline_env`` environment, type ::

        pip install easy-plot-beamline

If you prefer to install from sources, after installing the dependencies, obtain the source archive from
`GitHub <https://github.com/cadenmyers13/easy-plot-beamline/>`_. Once installed, ``cd`` into your ``easy-plot-beamline`` directory
and run the following ::

        pip install .

This package also provides command-line utilities. To check the software has been installed correctly, type ::

        easy-plot-beamline --version

You can also type the following command to verify the installation. ::

        python -c "import easy_plot_beamline; print(easy_plot_beamline.__version__)"


To view the basic usage and available commands, type ::

        easy-plot-beamline -h

Getting Started
---------------

You may consult our `online documentation <https://cadenmyers13.github.io/easy-plot-beamline>`_ for tutorials and API references.

Support and Contribute
----------------------

If you see a bug or want to request a feature, please `report it as an issue <https://github.com/cadenmyers13/easy-plot-beamline/issues>`_ and/or `submit a fix as a PR <https://github.com/cadenmyers13/easy-plot-beamline/pulls>`_.

Feel free to fork the project and contribute. To install easy-plot-beamline
in a development mode, with its sources being directly used by Python
rather than copied to a package directory, use the following in the root
directory ::

        pip install -e .

To ensure code quality and to prevent accidental commits into the default branch, please set up the use of our pre-commit
hooks.

1. Install pre-commit in your working environment by running ``conda install pre-commit``.

2. Initialize pre-commit (one time only) ``pre-commit install``.

Thereafter your code will be linted by black and isort and checked against flake8 before you can commit.
If it fails by black or isort, just rerun and it should pass (black and isort will modify the files so should
pass after they are modified). If the flake8 test fails please see the error messages and fix them manually before
trying to commit again.

Improvements and fixes are always appreciated.

Before contributing, please read our `Code of Conduct <https://github.com/cadenmyers13/easy-plot-beamline/blob/main/CODE-OF-CONDUCT.rst>`_.

Contact
-------

For more information on easy-plot-beamline please visit the project `web-page <https://cadenmyers13.github.io/>`_ or email Caden Myers at cjm2304@columbia.edu.

Acknowledgements
----------------

``easy-plot-beamline`` is built and maintained with `scikit-package <https://scikit-package.github.io/scikit-package/>`_.

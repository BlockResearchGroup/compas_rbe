********************************************************************************
Getting Started
********************************************************************************

Create environment
==================

.. code-block:: bash

    conda create -n rbe -c conda-forge python=3.7 COMPAS

.. note::

    On Mac, make sure to install the framework version of Python as well.

    ``conda create -n rbe -c conda-forge python=3.7 python.app COMPAS``

Activate environment
====================

.. code-block:: bash

    conda activate rbe

Install dependencies
====================

.. code-block:: bash

    conda install -c conda-forge cvxpy
    conda install -c conda-forge cvxopt
    conda install -c ibmdecisionoptimization cplex

Install the package
===================

.. code-block:: bash

    $ pip install git+https://github.com/BlockResearchGroup/compas_rbe.git#egg=compas_rbe

Check the installation
======================

Start an interactive Python interpreter on the command line, and import the installed packages.

.. code-block:: python

    >>> import compas
    >>> import compas_rbe

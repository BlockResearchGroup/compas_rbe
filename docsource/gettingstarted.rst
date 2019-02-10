********************************************************************************
Getting Started
********************************************************************************

.. highlight:: bash


Requirements
============

* `Anaconda <https://www.anaconda.com/download>`_
* `Github <https://github.com>`_ account
* `Git <https://git-scm.com/downloads>`_


Installation
============

.. note::

    If you intend to install ``compas_rbe`` in a virtual environment,
    make sure to activate the environment first.


1. Install dependencies
-----------------------

**On Mac**

::

    $ conda install -n rbe -c conda-forge cvxopt
    $ conda install -n rbe -c omnia cvxpy


**On Windows**

::

    $ pip install cvxopt
    $ pip install ecos
    $ pip install cvxpy


2. Install the package
----------------------

.. note::

    This will also install COMPAS and its dependencies, if necessary.

::

    $ pip install git+https://github.com/BlockResearchGroup/compas_rbe.git


3. Check installation
---------------------

Start an interactive Python session in the Terminal.

::

    >>> import compas
    >>> import compas_rbe


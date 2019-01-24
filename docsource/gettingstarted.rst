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

In this tutorial, we will create a new virtual environment with ``conda`` to install
``compas_rbe``. We will name the environment ``rbe``, but you can use any
name you like.

If you wish to install ``compas_rbe`` in an already existing environment, just
skip the first step and simply activate the environment of your choice.


1. Create a virtual environment and install COMPAS
--------------------------------------------------

* https://conda.io/projects/conda/en/latest/user-guide/getting-started.html#managing-environments

::

    $ conda create -n rbe -c conda-forge python=3.6 COMPAS


2. Activate the environment
---------------------------

* https://conda.io/projects/conda/en/latest/user-guide/getting-started.html#managing-environments


**On Mac**

::

    $ source activate rbe


**On Windows**

::

    $ activate rbe


3. Install dependencies
-----------------------

To install ``compas_assembly``, follow the instructions here
https://blockresearchgroup.github.io/compas_assembly/gettingstarted.html

The instructions below are for installing the solvers.

* http://cvxopt.org/install/index.html
* https://www.cvxpy.org/install/


**On Mac**

::

    $ conda install -n rbe -c conda-forge cvxopt
    $ conda install -n rbe -c omnia cvxpy


**On Windows**

* https://github.com/cvxgrp/cvxpy/issues/88

::

    $ pip install cvxopt
    $ pip install ecos
    $ pip install cvxpy


4. Fork package
----------------

* `COMPAS rbe <https://github.com/BlockResearchGroup/compas_rbe>`_


Go to https://github.com/BlockResearchGroup/compas_rbe and *fork* the repository to your
personal account. This will simplify the development process when you will start
making changes to the code or when you want to start contributing.


5. Clone forked package
-----------------------

* https://github.com/<your-username>/compas_rbe

Clone the forked package to a location on your computer.

::

    $ mkdir ~/Code/COMPAS-packages
    $ cd ~/Code/COMPAS-packages
    $ git clone https://github.com/<your-username>/compas_rbe.git


6. Install cloned package
-------------------------

::

    $ cd compas_rbe
    $ pip install -r requirements-dev.txt


7. Check installation
---------------------

Start an interactive Python session and import the installed packages.

>>> import compas
>>> import compas_rbe


8. Install packages for Rhino
-----------------------------

**On Mac**

::

    $ python -m compas_rhinomac.install compas compas_rhino compas_assembly compas_rbe


**On Windows**

*Not available yet.*


9. Install Rhino plugin
-----------------------

**On Mac**

::

    $ cd ui/RhinoMac
    $ python -m compas_rhino.install_plugin RBE{520ddb34-e56d-4a37-9c58-1da10edd1d62}


**On Windows**

*Not available yet.*


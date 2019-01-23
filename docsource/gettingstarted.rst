********************************************************************************
Getting Started
********************************************************************************

.. highlight:: bash


Create a virtual environment and install COMPAS
-----------------------------------------------

* https://conda.io/projects/conda/en/latest/user-guide/getting-started.html#managing-environments

::

    $ conda config --add channels conda-forge
    $ conda create -n rbe python=3.6 COMPAS


Activate the environment
------------------------

* https://conda.io/projects/conda/en/latest/user-guide/getting-started.html#managing-environments


**On Mac**

::

    $ source activate rbe

**On Windows**

::

    $ activate rbe


Install solvers
---------------

* http://cvxopt.org/install/index.html
* https://www.cvxpy.org/install/


**On Mac**

::

    $ conda install -n rbe -c cvxopt
    $ conda install -n rbe -c omnia cvxpy


**On Windows**

* https://github.com/cvxgrp/cvxpy/issues/88

::

    $ pip install cvxopt
    $ pip install ecos
    $ pip install cvxpy


Fork packages
-------------

* `COMPAS assembly <https://github.com/BlockResearchGroup/compas_assembly>`_
* `COMPAS rbe <https://github.com/BlockResearchGroup/compas_rbe>`_


Go to https://github.com/BlockResearchGroup and *fork* the repositories to your
personal account. This will simplify the development process when you will start
making changes to the code or when you want to start contributing.


Make a base folder
------------------

For example

::

    $ mkdir ~/Code/COMPAS-packages
    $ cd ~/Code/COMPAS-packages


Clone forked packages
---------------------

* https://github.com/<your-username>/compas_assembly
* https://github.com/<your-username>/compas_rbe

::

    $ git clone https://github.com/<your-username>/compas_assembly.git

::

    $ git clone https://github.com/<your-username>/compas_rbe.git


Install cloned packages
-----------------------

::

    $ cd ~/Code/COMPAS-packages/compas_assembly
    $ pip install -r requirements-dev.txt

::

    $ cd ~/Code/COMPAS-packages/compas_rbe
    $ pip install -r requirements-dev.txt


Check installation
------------------

Start an interactive Python session in the Terminal.

>>> import compas
>>> import compas_rhino
>>> import compas_assembly
>>> import compas_rbe


Install packages for Rhino
--------------------------

**On Mac**

::

    $ python -m compas_rhinomac.install compas compas_rhino compas_assembly compas_rbe


**On Windows**

*Not available yet.*


Install Rhino plugin
--------------------

**On Mac**

::

    $ cd ~/Code/COMPAS-packages/compas_rbe/ui/RhinoMac
    $ python -m compas_rhino.install_plugin RBE{520ddb34-e56d-4a37-9c58-1da10edd1d62}


**On Windows**

*Not available yet.*


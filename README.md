# COMPAS RBE

Rigid Block Equilibrium Analysis for the COMPAS framework


## Getting Started

1.  Create and/or activate a virtual environment

    ```bash
    $ conda create -n rbe
    $ source activate rbe
    ```

2.  Fork and clone `compas_assembly` and `compas_rbe`

    Make a base folder for `COMPAS` packages. For example

    ```bash
    $ mkdir ~/Code/COMPAS-packages 
    $ cd ~/Code/COMPAS-packages
    ```

    Clone `compas_assembly`

    ```bash
    $ git clone https://github.com/BlockResearchGroup/compas_assembly.git
    ```    

    Clone `compas_rbe`

    ```bash
    $ git clone https://github.com/BlockResearchGroup/compas_rbe.git
    ```    

3.  Pre-installation stuff

    ```bash
    $ conda install -n rbe COMPAS
    ```

4.  Install `compas_assembly` and `compas_rbe` from local source

    ```bash
    $ cd compas_assembly
    $ pip install -r requirements-dev.txt
    $ cd ..
    ```

    ```bash
    $ cd compas_rbe
    $ pip install -r requirements-dev.txt
    $ cd ..
    ```

7.  Check installation

    ```ipython
    >>> import compas
    >>> import compas_rhino
    >>> import compas_assembly
    >>> import compas_rbe
    ```

6.  Install `compas_rbe` for RhinoMac

    ```bash
    $ python -m compas_rhino.install_plugin RBE{520ddb34-e56d-4a37-9c58-1da10edd1d62}
    ```

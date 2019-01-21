# COMPAS RBE

Rigid Block Equilibrium Analysis for the COMPAS framework


## Getting Started

1.  Create a virtual environment and install COMPAS

    ```bash
    $ conda config --add channels conda-forge
    $ conda create -n rbe python=3.6 COMPAS
    ```

    or

    ```bash
    $ conda config --add channels conda-forge
    $ conda create -n rbe python=3.6
    $ conda install -n rbe COMPAS
    ```

2.  Activate the environment

    ```bash
    $ source activate rbe
    ```

    or, on Windows

    ```bash
    $ activate rbe
    ```

3.  Fork `compas_assembly` and `compas_rbe`

    Go to https://github.com/BlockResearchGroup and *fork* the repositories to your
    personal account. This will simplify the development process when you will start
    making changes to the code or when you want to start contributing.

4.  Clone `compas_assembly` and `compas_rbe` to your computer

    Make a base folder for `COMPAS` packages. For example

    ```bash
    $ mkdir ~/Code/COMPAS-packages 
    $ cd ~/Code/COMPAS-packages
    ```

    Clone `compas_assembly`

    ```bash
    $ git clone https://github.com/<your-username>/compas_assembly.git
    ```    

    Clone `compas_rbe`

    ```bash
    $ git clone https://github.com/<your-username>/compas_rbe.git
    ```    

5.  Install `compas_assembly` and `compas_rbe` from local source

    ```bash
    $ cd ~/Code/COMPAS-packages/compas_assembly
    $ pip install -r requirements-dev.txt
    ```

    ```bash
    $ cd ~/Code/COMPAS-packages/compas_rbe
    $ pip install -r requirements-dev.txt
    ```

6.  Check installation

    Start an interactive Python session in the Terminal.

    ```ipython
    >>> import compas
    >>> import compas_rhino
    >>> import compas_assembly
    >>> import compas_rbe
    ```

7.  Install `compas`, `compas_rhino`, `compas_assembly`, `compas_rbe` for RhinoMac

    ```bash
    $ python -m compas_rhinomac.install -p compas compas_rhino compas_assembly compas_rbe
    ```

8.  Install the `RBE` plugin for RhinoMac

    ```bash
    $ cd ~/Code/COMPAS-packages/compas_rbe/ui/RhinoMac
    $ python -m compas_rhino.install_plugin RBE{520ddb34-e56d-4a37-9c58-1da10edd1d62}
    ```


## Known Issues



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

2.  Install `cvxpy` and `cvxopt`

    ```bash
    $ conda install -n rbe -c omnia cvxpy
    $ conda install -n rbe -c anaconda cvxopt
    ```

3.  Install other solvers (optional)

    * `MOSEK`: `conda install -n rbe -c mosek mosek`
    * `CPLEX`: https://www.ibm.com/analytics/cplex-optimizer

4.  Activate the environment

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

4.  Make a base folder for `COMPAS` packages on your computer. For example

    ```bash
    $ mkdir ~/Code/COMPAS-packages 
    $ cd ~/Code/COMPAS-packages
    ```

5.  Clone `compas_assembly` and `compas_rbe`

    ```bash
    $ git clone https://github.com/<your-username>/compas_assembly.git
    ```    

    ```bash
    $ git clone https://github.com/<your-username>/compas_rbe.git
    ```    

6.  Install `compas_assembly` and `compas_rbe`

    ```bash
    $ cd ~/Code/COMPAS-packages/compas_assembly
    $ pip install -r requirements-dev.txt
    ```

    ```bash
    $ cd ~/Code/COMPAS-packages/compas_rbe
    $ pip install -r requirements-dev.txt
    ```

7.  Check installation

    Start an interactive Python session in the Terminal.

    ```ipython
    >>> import compas
    >>> import compas_rhino
    >>> import compas_assembly
    >>> import compas_rbe
    ```

8.  Install `compas`, `compas_rhino`, `compas_assembly`, `compas_rbe` for RhinoMac

    ```bash
    $ python -m compas_rhinomac.install compas compas_rhino compas_assembly compas_rbe
    ```

9.  Install the `RBE` plugin for RhinoMac

    ```bash
    $ cd ~/Code/COMPAS-packages/compas_rbe/ui/RhinoMac
    $ python -m compas_rhino.install_plugin RBE{520ddb34-e56d-4a37-9c58-1da10edd1d62}
    ```


## First Steps

Try one of the examples included in the `examples` folder.


## Known Issues

> Installing the plugin didn't work, but the installer said the process
  was completed successfully.

Try deleting the plugin manually and install it again.
You can find the installed plugin here:

```
~/Library/Application Support/McNeel/Rhinoceros/MacPlugIns/PythonPlugIns/RBE{...}
```

> The installation of `cvxpy` and/or `cvxopt` was aborted because `conda` was denied
  permission to install some of their dependencies.

If Anaconda was installed anywhere else than in your home directory, yuo may need
to run the `conda` commands using `sudo`.

```bash
$ sudo conda install -c omnia cvxpy
```

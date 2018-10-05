"""
********************************************************************************
compas_rbe
********************************************************************************

.. currentmodule:: compas_rbe


.. toctree::
    :maxdepth: 1

    compas_rbe.datastructures
    compas_rbe.equilibrium
    compas_rbe.rhino
    compas_rbe.viewer

"""

from __future__ import print_function

import os
import sys


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2017 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'
__version__   = '0.0.1'


HERE = os.path.dirname(__file__)

HOME = os.path.abspath(os.path.join(HERE, '../../'))
DATA = os.path.abspath(os.path.join(HOME, 'data'))
DOCS = os.path.abspath(os.path.join(HOME, 'docs'))
TEMP = os.path.abspath(os.path.join(HOME, 'temp'))

SRC = os.path.abspath(os.path.join(HOME, 'src'))


def _find_resource(filename):
    filename = filename.strip('/')
    return os.path.abspath(os.path.join(DATA, filename))


def get(filename):
    return _find_resource(filename)


def license():
    with open(os.path.join(HOME, 'LICENSE')) as fp:
        return fp.read()


def version():
    return __version__


def help():
    return 'http://compas-dev.github.io'


def copyright():
    return __copyright__


def credits():
    pass


def requirements():
    with open(os.path.join(HERE, '../requirements.txt')) as f:
        for line in f:
            print(line.strip())


__all__ = ['HOME', 'DATA', 'DOCS', 'TEMP', 'SRC', 'get', 'license', 'requirements', 'version']

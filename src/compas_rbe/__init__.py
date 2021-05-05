"""
********************************************************************************
compas_rbe
********************************************************************************

.. currentmodule:: compas_rbe


.. toctree::
    :maxdepth: 1

    compas_rbe.equilibrium

"""

from __future__ import print_function

import os


__author__ = 'Tom Van Mele'
__copyright__ = 'Copyright 2017 - Block Research Group, ETH Zurich'
__license__ = 'MIT License'
__email__ = 'vanmelet@ethz.ch'
__version__ = '0.1.2rc0'


HERE = os.path.dirname(__file__)

HOME = os.path.abspath(os.path.join(HERE, '../../'))
DATA = os.path.abspath(os.path.join(HOME, 'data'))
DOCS = os.path.abspath(os.path.join(HOME, 'docs'))
SRC = os.path.abspath(os.path.join(HOME, 'src'))

TEMP = os.path.abspath(os.path.join(HERE, '__temp'))


def _find_resource(filename):
    filename = filename.strip('/')
    return os.path.abspath(os.path.join(DATA, filename))


def get(filename):
    return _find_resource(filename)


__all__ = ['HOME', 'DATA', 'DOCS', 'SRC', 'TEMP', 'get']

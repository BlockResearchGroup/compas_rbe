from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas
import os

import ctypes
from ctypes import *

from compas.interop.cpp.xdarray import Array1D
from compas.interop.cpp.xdarray import Array2D


HERE = os.path.dirname(__file__)
SO = os.path.join(HERE, '_interfaceforces_igl', 'iforces.so')


__all__ = ['interfaceforces_igl']


def interfaceforces_igl():
    iforces = ctypes.cdll.LoadLibrary(SO)

    iforces.compute_iforces.argtypes = []

    iforces.compute_iforces()

    return 0


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    interfaceforces_igl()


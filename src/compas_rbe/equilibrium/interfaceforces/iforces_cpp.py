from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas
import os

import ctypes
from ctypes import c_int

from compas.interop.cpp.xdarray import Array1D
from compas.interop.cpp.xdarray import Array2D


HERE = os.path.dirname(__file__)
SO = os.path.join(HERE, '_iforces_cpp', 'iforces_cpp.so')


__all__ = ['iforces_cpp']


def iforces_cpp(vertices):
    iforces = ctypes.cdll.LoadLibrary(SO)

    c_vertices = Array2D(vertices, 'double')

    iforces.compute_iforces.argtypes = [
        c_int,
        c_vertices.ctype
    ]

    iforces.compute_iforces(
        c_int(len(vertices)),
        c_vertices.cdata
    )

    return 0


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import compas
    from compas.datastructures import Mesh

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    vertices = mesh.get_vertices_attributes('xyz')

    print(vertices)

    iforces_cpp(vertices)

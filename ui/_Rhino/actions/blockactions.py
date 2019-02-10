from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os

import compas
import compas_rhino
import compas_rbe

from compas_rbe.datastructures import Assembly
from compas_rbe.rhino import AssemblyArtist
from compas_rbe.rhino import BlockArtist

HERE = os.path.abspath(os.path.dirname(__file__))

try:
    import rhinoscriptsyntax as rs
except ImportError:
    pass


__all__ = ['BlockActions']


class BlockActions(object):

    def blocks_from_polysurfaces(self):
        pass

    def blocks_from_meshes(self):
        pass


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass

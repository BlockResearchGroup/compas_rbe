from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rbe.rbe import Block

from compas_rhino.helpers import MeshArtist


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__   = 'MIT license'
__email__     = 'vanmelet@ethz.ch'


__all__ = ['Block', ]


class Block(Block):
    """"""

    def __init__(self):
        super(Block, self).__init__()

    @classmethod
    def from_polysurface(cls, guid):
        return compas_rhino.mesh_from_surface(cls, guid)

    def draw(self, layer=None):
        raise NotImplementedError


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass

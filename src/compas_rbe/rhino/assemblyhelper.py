from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

from compas_rhino.selectors import VertexSelector
from compas_rhino.selectors import EdgeSelector
from compas_rhino.modifiers import VertexModifier
from compas_rhino.modifiers import EdgeModifier


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__   = 'MIT license'
__email__     = 'vanmelet@ethz.ch'


__all__ = ['AssemblyHelper']


class AssemblyHelper(VertexSelector,
                     EdgeSelector,
                     VertexModifier,
                     EdgeModifier):

    pass


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass

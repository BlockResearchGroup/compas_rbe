from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

from compas_rhino.selectors import VertexSelector
from compas_rhino.selectors import EdgeSelector
from compas_rhino.selectors import FaceSelector
from compas_rhino.modifiers import VertexModifier
from compas_rhino.modifiers import EdgeModifier
from compas_rhino.modifiers import FaceModifier


__all__ = ['AssemblyHelper', 'BlockHelper']


class AssemblyHelper(VertexSelector,
                     EdgeSelector,
                     VertexModifier,
                     EdgeModifier):

    pass    


class BlockHelper(VertexSelector,
                  EdgeSelector,
                  FaceSelector,
                  VertexModifier,
                  EdgeModifier,
                  FaceModifier):

    pass


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass

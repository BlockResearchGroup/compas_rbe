from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os

import compas
import compas_rhino
import compas_rbe

from compas_rbe.datastructures import Assembly
from compas_rbe.rhino import AssemblyArtist

HERE = os.path.abspath(os.path.dirname(__file__))

try:
    import rhinoscriptsyntax as rs
except ImportError:
    pass


__all__ = ['AssemblyActions']


class AssemblyActions(object):

    def assembly_from_json(self):
        pass

    def assembly_to_json(self):
        pass

    def assembly_update_vertex_attr(self):
        pass

    def assembly_update_edge_attr(self):
        pass

    def assembly_select_vertices(self):
        pass

    def assembly_select_edges(self):
        pass


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import ast

import compas_rhino

from compas_rbe.rbe import Assembly
from compas_rbe.cad.rhino import Block

from compas_rhino.helpers.selectors import VertexSelector
from compas_rhino.helpers.selectors import EdgeSelector
from compas_rhino.helpers.modifiers import VertexModifier
from compas_rhino.helpers.modifiers import EdgeModifier


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__   = 'MIT license'
__email__     = 'vanmelet@ethz.ch'


__all__ = ['Assembly']


# make this into an "AssemblyObject"?
# ao.datastructure
# ao.artist = NetworkArtist(self)
class Assembly(Assembly):
    """"""

    select_vertices = VertexSelector.select_vertices
    select_edges = EdgeSelector.select_edges

    update_vertex_attributes = VertexModifier.update_vertex_attributes
    update_edge_attributes = EdgeModifier.update_edge_attributes

    def __init__(self):
        super(Assembly, self).__init__()

    @classmethod
    def from_polysurfaces(cls, guids):
        names = compas_rhino.get_object_names(guids)
        assembly = cls()
        for i, guid in enumerate(guids):
            name = names[i]
            try:
                attr = ast.literal_eval(name)
            except (TypeError, ValueError):
                attr = {}
            name = attr.get('name', 'B{0}'.format(i))
            block = Block.from_polysurface(guid)
            block.attributes['name'] = name
            assembly.add_block(block, attr_dict=attr)
        return assembly

    @classmethod
    def from_meshes(cls, guids):
        names = compas_rhino.get_object_names(guids)
        assembly = cls()
        for i, guid in enumerate(guids):
            name = names[i]
            try:
                attr = ast.literal_eval(name)
            except (TypeError, ValueError):
                attr = {}
            name = attr.get('name', 'B{0}'.format(i))
            block = compas_rhino.mesh_from_guid(Block, guid)
            block.attributes['name'] = name
            assembly.add_block(block, attr_dict=attr)
        return assembly


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass

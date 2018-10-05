from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import ast

from compas.datastructures import Network


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__   = 'MIT license'
__email__     = 'vanmelet@ethz.ch'


__all__ = ['Assembly']


class Assembly(Network):
    """"""

    def __init__(self):
        super(Assembly, self).__init__()
        self.blocks = {}
        self.attributes.update({
            'name': 'Assembly'
        })
        self.default_vertex_attributes.update({
            'is_support': False
        })
        self.default_edge_attributes.update({
            'interface_points' : None,
            'interface_type'   : None,
            'niterface_size'   : None,
            'interface_uvw'    : None,
            'interface_origin' : None,
            'interface_forces' : None,
        })

    # from/to data
    # from/to json

    @classmethod
    def from_polysurfaces(cls, guids):
        import compas_rhino
        from compas_rbe.assemblies import Block

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
        import compas_rhino
        from compas_rhino.helpers import mesh_from_guid
        from compas_rbe.assemblies import Block

        names = compas_rhino.get_object_names(guids)
        assembly = cls()

        for i, guid in enumerate(guids):
            name = names[i]

            try:
                attr = ast.literal_eval(name)
            except (TypeError, ValueError):
                attr = {}

            name = attr.get('name', 'B{0}'.format(i))
            block = mesh_from_guid(Block, guid)
            block.attributes['name'] = name
            assembly.add_block(block, attr_dict=attr)

        return assembly

    def add_block(self, block, attr_dict=None, **kwattr):
        attr = attr_dict or {}
        attr.update(kwattr)
        x, y, z = block.centroid()
        key = self.add_vertex(attr_dict=attr, x=x, y=y, z=z)
        self.blocks[key] = block

    def add_support(self, block, attr_dict=None, **kwattr):
        x, y, z = block.centroid()
        key = self.add_vertex(x=x, y=y, z=z, is_support=True)
        self.blocks[key] = block


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass

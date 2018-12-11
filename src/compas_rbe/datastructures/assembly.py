from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import ast
import json

from compas.datastructures import Network


__all__ = ['Assembly']


# should an assembly be composed of a network attribute
# and a block collection
# rather than inherit from network
# and add inconsistent stuff to that interface?


class Assembly(Network):
    """A data structure for discrete element assemblies.

    Attributes
    ----------
    blocks : dict
        A dictionary of blocks, with each block represented by a mesh.

    Examples
    --------
    .. code-block:: python



    """

    __module__ = 'compas_rbe.datastructures'

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

    @classmethod
    def from_json(cls, filepath):
        from compas_rbe.datastructures import Block

        with open(filepath, 'r') as fo:
            data = json.load(fo)

            # vertex keys in an assembly can be of any hashable type
            # keys in the blocks dict should be treated the same way!

            assembly = cls.from_data(data['assembly'])
            assembly.blocks = {int(key): Block.from_data(data['blocks'][key]) for key in data['blocks']}

        return assembly

    def to_json(self, filepath):
        data = {
            'assembly' : self.to_data(),
            'blocks': {str(key): self.blocks[key].to_data() for key in self.blocks}
        }
        with open(filepath, 'w') as fo:
            json.dump(data, fo)

    def add_block(self, block, attr_dict=None, **kwattr):
        """Add a block to the assembly.

        Parameters
        ----------
        block : compas_rbe.datastructures.Block
            The block to add.
        attr_dict : dict, optional
            A dictionary of block attributes.
            Default is ``None``.

        Returns
        -------
        hashable
            The identifier of the block.

        Notes
        -----
        The block is added as a vertex in the assembly data structure.
        The XYZ coordinates of the vertex are the coordinates of the centroid of the block.

        """
        attr = attr_dict or {}
        attr.update(kwattr)
        x, y, z = block.centroid()
        key = self.add_vertex(attr_dict=attr, x=x, y=y, z=z)
        self.blocks[key] = block
        return key

    def add_blocks_from_polysurfaces(self, guids):
        """Add multiple blocks from their representation as Rhino poly surfaces.

        Parameters
        ----------
        guids : list of str
            A list of GUIDs identifying the poly-surfaces representing the blocks of the assembly.

        Returns
        -------
        list
            The keys of the added blocks.

        Warning
        -------
        This method only works in Rhino.

        Examples
        --------
        .. code-block:: python

            pass

        """
        from compas_rbe.datastructures import Block

        onames = compas_rhino.get_object_names(guids)

        keys = []

        for i, (guid, oname) in enumerate(zip(guids, onames)):
            try:
                attr = ast.literal_eval(oname)
            except (TypeError, ValueError):
                attr = {}

            name = attr.get('name', 'B{0}'.format(i))

            block = Block.from_polysurface(guid)
            block.attributes['name'] = name

            key = self.add_block(block, attr_dict=attr)

            keys.append(key)

        return keys

    def add_blocks_from_rhinomeshes(self, guids):
        """Add multiple blocks from their representation as as Rhino meshes.

        Parameters
        ----------
        guids : list of str
            A list of GUIDs identifying the meshes representing the blocks of the assembly.

        Returns
        -------
        list
            The keys of the added blocks.

        Warning
        -------
        This method only works in Rhino.

        Examples
        --------
        .. code-block:: python

            pass

        """
        from compas_rbe.datastructures import Block

        onames = compas_rhino.get_object_names(guids)

        keys = []

        for i, (guid, oname) in enumerate(zip(guids, onames)):
            try:
                attr = ast.literal_eval(oname)
            except (TypeError, ValueError):
                attr = {}

            name = attr.get('name', 'B{0}'.format(i))

            block = Block.from_rhinomesh(guid)
            block.attributes['name'] = name

            key = self.add_block(block, attr_dict=attr)

            keys.append(key)

        return keys

    def add_support(self, block, attr_dict=None, **kwattr):
        """Add a support to the assembly.

        Parameters
        ----------
        block : compas_rbe.datastructures.Block
            The block to add.
        attr_dict : dict, optional
            A dictionary of block attributes.
            Default is ``None``.

        Returns
        -------
        hashable
            The identifier of the block.

        Notes
        -----
        The support block is added as a vertex in the assembly data structure.
        The XYZ coordinates of the vertex are the coordinates of the centroid of the block.

        """
        x, y, z = block.centroid()
        key = self.add_vertex(x=x, y=y, z=z, is_support=True)
        self.blocks[key] = block
        return key

    def draw(self, settings=None):
        """Convenience function for drawing the assembly in Rhino using common visualisation settings.

        Parameters
        ----------
        settings : dict, optional
            A dictionary with drawing options.

        """
        from compas_rbe.rhino import AssemblyArtist

        settings = settings or {}

        artist = AssemblyArtist(self, layer=settings.get('layer'))

        artist.defaults.update({key: settings[key] for key in settings if key.startswith('color') or key.startswith('scale') or key.startswith('eps')})

        artist.clear_layer()
        artist.draw_blocks()

        if settings.get('show.vertices'):
            artist.draw_vertices(
                color={key: settings.get('color.vertex:is_support') for key in self.vertices_where({'is_support': True})}
            )
        if settings.get('show.edges'):
            artist.draw_edges()
        if settings.get('show.interfaces'):
            artist.draw_interfaces()
        if settings.get('show.forces') or True:
            artist.draw_forces()
        if settings.get('show.selfweight'):
            artist.draw_selfweight()

        artist.redraw()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass

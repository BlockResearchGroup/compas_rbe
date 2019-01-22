from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_assembly.datastructures import Assembly as Assembly_


__all__ = ['Assembly']


# should an assembly be composed of a network attribute
# and a block collection
# rather than inherit from network
# and add inconsistent stuff to that interface?


class Assembly(Assembly_):

    __module__ = 'compas_rbe.datastructures'

    def add_support(self, block, attr_dict=None, **kwattr):
        """Add a support to the assembly.

        Parameters
        ----------
        block : compas_assembly.datastructures.Block
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

        artist.defaults.update({
            key: settings[key]
            for key in settings if key.startswith('color') or
            key.startswith('scale') or key.startswith('eps')
        })

        artist.clear_layer()
        artist.draw_blocks()

        if settings.get('show.vertices'):
            artist.draw_vertices(
                color={
                    key: settings.get('color.vertex:is_support')
                    for key in self.vertices_where({
                        'is_support': True
                    })
                })
        if settings.get('show.edges'):
            artist.draw_edges()
        if settings.get('show.interfaces'):
            artist.draw_interfaces()
        if settings.get('show.forces'):
            if settings.get('mode.interface') == 0:
                artist.color_interfaces(0)
            else:
                artist.color_interfaces(1)
            if settings.get('show.forces_as_vectors'):
                if settings.get('mode.force') == 0:
                    artist.draw_forces(mode=0)
                else:
                    artist.draw_forces(mode=1)
        if settings.get('show.selfweight'):
            artist.draw_selfweight()
        if settings.get('show.frictions'):
            if settings.get('mode.friction') == 0:
                artist.draw_frictions(mode=0)
            else:
                artist.draw_frictions(mode=1)

        artist.redraw()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass

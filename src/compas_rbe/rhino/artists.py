from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import i_to_blue

import compas_rhino

from compas_rhino.artists import MeshArtist
from compas_rhino.artists import NetworkArtist


__all__ = ['AssemblyArtist', 'BlockArtist']


class AssemblyArtist(NetworkArtist):
    """An artist for visualisation of assemblies inn Rhino.

    Parameters
    ----------
    assembly : compas_rbe.datastructures.Assembly
        The assembly data structure.
    layer : str, optional
        The base layer for drawing.
        Default is ``None``, which means drawing in the current layer.

    Examples
    --------
    .. code-block:: python

        pass

    """

    def __init__(self, assembly, layer=None):
        super(AssemblyArtist, self).__init__(assembly, layer=layer)
        self.defaults.update({

        })

    @property
    def assembly(self):
        """Assembly : the assembly data structure."""
        return self.datastructure
    
    @assembly.setter
    def assembly(self, assembly):
        self.datastructure = assembly

    def draw_blocks(self, show_faces=False, show_vertices=False):
        """Draw the blocks of the assembly.

        Parameters
        ----------
        show_faces : bool, optional
            Draw the faces of the block.
            Default is ``False``.
        show_vertices : bool, optional
            Draw the vertices of the block.
            Default is ``False``.

        Notes
        -----
        * By default, blocks are drawn as wireframes.
        * By default, blocks are drawn on a sublayer of the base layer, if a base layer was specified.
        * Block names have the following pattern: ``"{assembly_name}.block.{block_id}"``
        * Faces and vertices can be drawn using the corresponding flags.
        * Block components have the following pattern: 

          * face: ``"{assembly_name}.block.{block_id}.face.{face_id}"``
          * edge: ``"{assembly_name}.block.{block_id}.edge.{edge_id}"``
          * vertex: ``"{assembly_name}.block.{block_id}.vertex.{vertex_id}"``


        Examples
        --------
        .. code-block:: python
        
            pass

        """
        layer = "{}::Blocks".format(self.layer) if self.layer else None
        artist = BlockArtist(None, layer=layer)
        for key, attr in self.assembly.vertices(True):
            block = self.assembly.blocks[key]
            block.name = "{}.block.{}".format(self.assembly.name, key)
            artist.block = block
            artist.draw_edges()
            if show_faces:
                artist.draw_faces()
            if show_vertices:
                artist.draw_vertices()
        artist.redraw()

    def draw_interfaces(self):
        layer = "{}::Interfaces".format(self.layer) if self.layer else None
        faces = []
        for u, v, attr in self.assembly.edges(True):
            points = attr['interface_points']
            faces.append({
                'points': points,
                'name'  : "{}.interface.{}-{}".format(self.assembly.name, u, v),
                'color' : (255, 255, 255)
            })
        compas_rhino.xdraw_faces(faces, layer=layer, clear=False, redraw=False)

    def draw_forces(self, scale=None, eps=None):
        layer = "{}::Forces".format(self.layer) if self.layer else None
        scale = scale or 0.1
        eps = eps or 1e-3
        lines = []

        for a, b, attr in self.assembly.edges(True):
            if attr['interface_forces']:
                w = attr['interface_uvw'][2]

                for i in range(len(attr['interface_points'])):
                    sp   = attr['interface_points'][i]
                    c_np = attr['interface_forces'][i]['c_np']
                    c_nn = attr['interface_forces'][i]['c_nn']

                    if scale * c_np > eps:
                        # compression force
                        lines.append({
                            'start' : sp,
                            'end'   : [sp[axis] + scale * c_np * w[axis] for axis in range(3)],
                            'color' : (0, 0, 255),
                            'name'  : "{0}.force.{1}-{2}.{3}".format(self.assembly.name, a, b, i),
                            'arrow' : 'end'
                        })
                    if scale * c_nn > eps:
                        # tension force
                        lines.append({
                            'start' : sp,
                            'end'   : [sp[axis] - scale * c_nn * w[axis] for axis in range(3)],
                            'color' : (255, 0, 0),
                            'name'  : "{0}.force.{1}-{2}.{3}".format(self.assembly.name, a, b, i),
                            'arrow' : 'end'
                        })

        compas_rhino.xdraw_lines(lines, layer=layer, clear=False, redraw=False)

    def draw_selfweight(self, scale=None, eps=None):
        pass

    # def color_interfaces(self):
    #     for u, v, attr in self.assembly.edges(True):
    #         name = "{}.interface.{}-{}".format(self.assembly.name, u, v)
    #         guids = compas_rhino.get_objects(name=name)
    #         if not guids:
    #             continue
    #         guid = guids[0]
    #         call = [force['c_np'] for force in attr['interface_forces']]
    #         cmax = max(call)
    #         cmin = 0
    #         colors = []
    #         for i in range(len(attr['interface_points'])):
    #             c = attr['interface_forces'][i]['c_np']
    #             blue = i_to_blue((c - cmin) / (cmax - cmin))
    #             colors.append(blue)
    #         compas_rhino.set_mesh_vertex_colors(guid, colors)


class BlockArtist(MeshArtist):

    def __init__(self, *args, **kwargs):
        super(BlockArtist, self).__init__(*args, **kwargs)
        self.defaults.update({

        })

    @property
    def block(self):
        return self.datastructure
    
    @block.setter
    def block(self, block):
        self.datastructure = block


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass

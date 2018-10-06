from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import i_to_blue

import compas_rhino

from compas_rhino.artists import MeshArtist
from compas_rhino.artists import NetworkArtist


__all__ = ['AssemblyArtist', 'BlockArtist']


class AssemblyArtist(NetworkArtist):

    def __init__(self, *args, **kwargs):
        super(AssemblyArtist, self).__init__(*args, **kwargs)
        self.defaults.update({

        })

    @property
    def assembly(self):
        return self.datastructure
    
    @assembly.setter
    def assembly(self, assembly):
        self.datastructure = assembly

    def draw_blocks(self):
        layer = "{}::Blocks".format(self.layer) if self.layer else None
        artist = BlockArtist(None, layer=layer)
        for key, attr in self.assembly.vertices(True):
            block = self.assembly.blocks[key]
            block.name = "{}.block.{}".format(self.assembly.name, key)
            artist.block = block
            artist.draw_edges()
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

    def color_interfaces(self):
        for u, v, attr in self.assembly.edges(True):
            name = "{}.interface.{}-{}".format(self.assembly.name, u, v)
            guids = compas_rhino.get_objects(name=name)
            if not guids:
                continue
            guid = guids[0]
            call = [force['c_np'] for force in attr['interface_forces']]
            cmax = max(call)
            cmin = 0
            colors = []
            for i in range(len(attr['interface_points'])):
                c = attr['interface_forces'][i]['c_np']
                blue = i_to_blue((c - cmin) / (cmax - cmin))
                colors.append(blue)
            compas_rhino.set_mesh_vertex_colors(guid, colors)


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

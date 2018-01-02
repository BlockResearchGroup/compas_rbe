from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import centroid_points
from compas.geometry import cross_vectors
from compas.geometry import normalize_vector
from compas.geometry import center_of_mass_polyhedron
from compas.geometry import volume_polyhedron

from compas.datastructures.mesh import Mesh


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__   = 'MIT license'
__email__     = 'vanmelet@ethz.ch'


class Block(Mesh):
    """"""

    def __init__(self):
        super(Block, self).__init__()
        self.attributes.update({
            'name': 'Block'
        })
        self.default_vertex_attributes.update({})
        self.default_edge_attributes.update({})

    def centroid(self):
        return centroid_points([self.vertex_coordinates(key) for key in self.vertices()])

    def frames(self):
        return {fkey: self.frame(fkey) for fkey in self.faces()}

    def frame(self, fkey):
        xyz = self.face_coordinates(fkey)
        o = xyz[0]
        w = self.face_normal(fkey)
        u = [xyz[1][i] - o[i] for i in range(3)]
        v = cross_vectors(w, u)
        uvw = normalize_vector(u), normalize_vector(v), normalize_vector(w)
        return o, uvw

    def center(self):
        vertices = [self.vertex_coordinates(key) for key in self.vertices()]
        faces = [self.face_vertices(fkey) for fkey in self.faces()]
        return center_of_mass_polyhedron((vertices, faces))

    def volume(self):
        return volume_polyhedron(self)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass

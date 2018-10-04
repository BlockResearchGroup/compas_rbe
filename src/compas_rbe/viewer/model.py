from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


from compas.utilities import pairwise


__all__ = ['BlockView']


class BlockView(object):
    
    def __init__(self, block):
        self._block = None
        self._xyz = None
        self._vertices = None
        self._faces = None
        self.block = block

    @property
    def block(self):
        return self._block

    @property
    def xyz(self):
        return self._xyz

    @property
    def vertices(self):
        return self.block.vertices()

    @property
    def faces(self):
        return self._faces

    @property
    def edges(self):
        key_index = self.block.key_index()
        for u, v in self.block.edges():
            yield key_index[u], key_index[v]

    @block.setter
    def block(self, block):
        self._block = block

        key_index = block.key_index()
        xyz = block.get_vertices_attributes('xyz')
        faces = []

        for fkey in block.faces():
            fvertices = [key_index[key] for key in block.face_vertices(fkey)]

            f = len(fvertices)
            if f < 3:
                pass
            elif f == 3:
                faces.append(fvertices)
            elif f == 4:
                a, b, c, d = fvertices
                faces.append([a, b, c])
                faces.append([c, d, a])
            else:
                o = block.face_centroid(fkey)
                v = len(xyz)
                xyz.append(o)
                for a, b in pairwise(fvertices + fvertices[0:1]):
                    faces.append([a, b, v])

        self._xyz = xyz
        self._faces = faces


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass

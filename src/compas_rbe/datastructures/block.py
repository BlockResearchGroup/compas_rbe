from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import centroid_points
from compas.geometry import cross_vectors
from compas.geometry import normalize_vector
from compas.geometry import centroid_polyhedron
from compas.geometry import volume_polyhedron

from compas.datastructures import Mesh


__all__ = ['Block']


class Block(Mesh):
    """A data structure for the individual blocks of a discrete block assembly.

    Examples
    --------
    .. code-block:: python
    
        pass

    """

    def __init__(self):
        super(Block, self).__init__()
        self.attributes.update({
            'name': 'Block'
        })
        self.default_vertex_attributes.update({})
        self.default_edge_attributes.update({})

    @classmethod
    def from_polysurface(cls, guid):
        """Class method for constructing a block fro a Rhino poly-surface.

        Parameters
        ----------
        guid : str
            The GUID of the poly-surface.

        Returns
        -------
        Block
            The block corresponding to the poly-surface.

        Notes
        -----
        In Rhino, poly-surfaces are organised such that the cycle directions of
        the individual sub-surfaces produce normal vectors that point out of the
        enclosed volume. The normal vectors of the faces of the mesh, therefore
        also point "out" of the enclosed volume.

        """
        from compas_rhino.helpers import mesh_from_surface
        return mesh_from_surface(cls, guid)

    def centroid(self):
        """Compute the centroid of the block.

        Returns
        -------
        point
            The XYZ location of the centroid.

        """
        return centroid_points([self.vertex_coordinates(key) for key in self.vertices()])

    def frames(self):
        """Compute the local frame of each face of the block.

        Returns
        -------
        dict
            A dictionary mapping face identifiers to face frames.

        """
        return {fkey: self.frame(fkey) for fkey in self.faces()}

    def frame(self, fkey):
        """Compute the frame of a specific face.

        Parameters
        ----------
        fkey : hashable
            The identifier of the frame.

        Returns
        -------
        frame
            The frame of the specified face.

        """
        xyz = self.face_coordinates(fkey)
        o = xyz[0]
        w = self.face_normal(fkey)
        u = [xyz[1][i] - o[i] for i in range(3)]
        v = cross_vectors(w, u)
        uvw = normalize_vector(u), normalize_vector(v), normalize_vector(w)
        return o, uvw

    def center(self):
        """Compute the center of mass of the block.

        Returns
        -------
        point
            The center of mass of the block.

        """
        vertices = [self.vertex_coordinates(key) for key in self.vertices()]
        faces = [self.face_vertices(fkey) for fkey in self.faces()]
        return centroid_polyhedron((vertices, faces))

    def volume(self):
        """Compute the volume of the block.

        Returns
        -------
        float
            The volume of the block.

        """
        vertices = [self.vertex_coordinates(key) for key in self.vertices()]
        faces = [self.face_vertices(fkey) for fkey in self.faces()]
        v = volume_polyhedron((vertices, faces))
        return v


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass

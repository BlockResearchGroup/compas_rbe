from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os

import compas
import compas_rhino
import compas_rbe

from compas.geometry import subtract_vectors

from compas_rbe.datastructures import Assembly
from compas_rbe.rhino import AssemblyArtist
from compas_rbe.rhino import AssemblyHelper

HERE = os.path.abspath(os.path.dirname(__file__))

try:
    import rhinoscriptsyntax as rs
except ImportError:
    pass


__all__ = ['AssemblyActions']


class AssemblyActions(object):

    def assembly_from_json(self):
        path = compas_rhino.select_file(folder=compas_rbe.DATA, filter='JSON files (*.json)|*.json||')
        if not path:
            return
        self.assembly = assembly = Assembly.from_json(path)
        self.assembly.draw(self.settings['layer'])

    def assembly_to_json(self):
        pass

    def assembly_update_vertex_attr(self):
        keys = AssemblyHelper.select_vertices(self.assembly)
        if not keys:
            return
        if AssemblyHelper.update_vertex_attributes(self.assembly, keys):
            self.assembly.draw(self.settings['layer'])

    def assembly_update_edge_attr(self):
        keys = AssemblyHelper.select_edges(self.assembly)
        if not keys:
            return
        if AssemblyHelper.update_edge_attributes(self.assembly, keys):
            self.assembly.draw(self.settings['layer'])

    def assembly_select_vertices(self):
        AssemblyHelper.select_vertices(self.assembly)

    def assembly_select_edges(self):
        pass

    def assembly_move_vertex(self):
        key = AssemblyHelper.select_vertex(self.assembly)
        if key is None:
            return

        block = self.assembly.blocks[key]

        xyz_before = self.assembly.get_vertex_attributes(key, 'xyz')
        AssemblyHelper.move_vertex(self.assembly, key)
        xyz_after = self.assembly.get_vertex_attributes(key, 'xyz')

        translation = subtract_vectors(xyz_after, xyz_before)

        for key, attr in block.vertices(True):
            attr['x'] += translation[0]
            attr['y'] += translation[1]
            attr['z'] += translation[2]

        self.assembly.draw(self.settings['layer'])


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass

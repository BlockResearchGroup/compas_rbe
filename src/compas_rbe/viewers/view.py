from __future__ import print_function

import sys

from PySide.QtCore import Qt

from compas.geometry import centroid_points

from compas.viewers.core.drawing import xdraw_polygons
from compas.viewers.core.drawing import xdraw_lines
from compas.viewers.core.drawing import xdraw_points

sys.path.insert(0, '/Users/vanmelet/Code/BlockResearchGroup/compas-apps/meshlab/src')

from widgets.glview import GLView


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = ['View', ]


class View(GLView):
    """"""

    def __init__(self, assembly):
        super(View, self).__init__()
        self.interfaces_on = Qt.Checked
        self.vertices_on = Qt.Unchecked
        self.edges_on = Qt.Checked
        self.faces_on = Qt.Unchecked
        self.forces_on = Qt.Checked
        self.assembly = assembly
        self.dx = 0
        self.dy = 0
        self.dz = 0
        self.center()

    def center(self):
        if not self.assembly:
            return
        cx, cy, cz = centroid_points([self.assembly.vertex_coordinates(key) for key in self.assembly.vertices()])
        for key, attr in self.assembly.vertices(True):
            attr['x'] -= cx
            attr['y'] -= cy
            block = self.assembly.blocks[key]
            for key, attr in block.vertices(True):
                attr['x'] -= cx
                attr['y'] -= cy
        for u, v, attr in self.assembly.edges(True):
            points = attr['interface_points']
            attr['interface_points']     = [[x - cx, y - cy, z] for x, y, z in points]
            attr['interface_origin'][0] -= cx
            attr['interface_origin'][1] -= cy

    def paint(self):
        if not self.assembly:
            return
        # blocks
        for key, attr in self.assembly.vertices(True):
            block = self.assembly.blocks[key]
            if self.edges_on:
                lines = []
                for u, v in block.edges():
                    lines.append({
                        'start': block.vertex_coordinates(u),
                        'end'  : block.vertex_coordinates(v),
                        'color': (0.1, 0.1, 0.1),
                        'width': 1.
                    })
                xdraw_lines(lines)
            if self.faces_on:
                polygons = []
                for fkey in block.faces():
                    points = block.face_coordinates(fkey)
                    color_front = (0.9, 0.9, 0.9, 0.5)
                    color_back  = (0.9, 0.9, 0.9, 0.5)
                    polygons.append({'points': points,
                                     'color.front': color_front,
                                     'color.back' : color_back})
                xdraw_polygons(polygons)
            if self.vertices_on:
                pass
        # interfaces
        if self.interfaces_on:
            polygons = []
            color_front = (0.2, 0.2, 0.2, 1.0)
            color_back  = (0.2, 0.2, 0.2, 1.0)
            for u, v, attr in self.assembly.edges(True):
                if attr['interface_type'] == 'face_face':
                    polygons.append({
                        'points'     : attr['interface_points'],
                        'color.front': color_front,
                        'color.back' : color_back
                    })
            xdraw_polygons(polygons)
        # forces
        if self.forces_on:
            lines = []
            for u, v, attr in self.assembly.edges(True):
                if attr['interface_forces']:
                    w = attr['interface_uvw'][2]
                    for i in range(len(attr['interface_points'])):
                        sp   = attr['interface_points'][i]
                        c_np = attr['interface_forces'][i]['c_np']
                        c_nn = attr['interface_forces'][i]['c_nn']
                        if c_np:
                            lines.append({
                                'start' : sp,
                                'end'   : [sp[axis] + 0.05 * c_np * w[axis] for axis in range(3)],
                                'color' : (0.0, 0.0, 1.0),
                                'width' : 3.0
                            })
                        if c_nn:
                            lines.append({
                                'start' : sp,
                                'end'   : [sp[axis] - 0.05 * c_nn * w[axis] for axis in range(3)],
                                'color' : (1.0, 0.0, 0.0),
                                'width' : 3.0
                            })
            xdraw_lines(lines)

    def keyPressAction(self, key):
        pass


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    pass

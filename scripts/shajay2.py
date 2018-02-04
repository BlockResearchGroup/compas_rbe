from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
import sys
import json

import compas
import compas_rhino
import compas_rbe

from compas.geometry import transpose_matrix
from compas.geometry import transform

from compas_rbe.rbe import Assembly
from compas_rbe.rbe import Block

from compas_rhino.helpers import MeshArtist


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'
__all__       = []


folder = os.path.join(compas_rbe.DATA, 'shajay/test2/objs')
files = [file for file in os.listdir(folder) if file.endswith('.obj')]
files = sorted(files, key=lambda x: int(x[1:-4]))

# print(files)

# artist = MeshArtist(None, layer='test')
# artist.clear_layer()

blocks = []
for file in files:
    block = Block.from_obj(os.path.join(folder, file))
    blocks.append(block)
    # artist.datastructure = block
    # artist.draw_faces()
    # artist.draw_edges()
    # artist.draw_vertices()

# artist.redraw()

# xforms = []
# centroids = []
# axes = []
# with open(os.path.join(folder, 'xform.txt')) as f:
#     for line in f.readlines()[:10]:
#         X, Y, Z, C = [[float(axis) if axis else 0.0 for axis in row.split(',')] for row in line.strip().split(' ')]
#         centroids.append(C)
#         axes.append((X, Y, Z))
#        X = transpose_matrix(X)
#        X.append([0.0, 0.0, 0.0, 1.0])
#        xforms.append(X)

# points = [
#     {
#         'pos' : xyz,
#         'name': 'B{}.centroid'.format(i)
#     }
#     for i, xyz in enumerate(centroids)
# ]
# xlines = [
#     {
#         'start': centroids[i],
#         'end'  : [centroids[i][j] + X[j] for j in range(3)],
#         'name' : 'B{}.X'.format(i),
#         'arrow': 'end',
#         'color': (255, 0, 0)
#     }
#     for i, (X, Y, Z) in enumerate(axes)
# ]
# ylines = [
#     {
#         'start': centroids[i],
#         'end'  : [centroids[i][j] + Y[j] for j in range(3)],
#         'name' : 'B{}.Y'.format(i),
#         'arrow': 'end',
#         'color': (0, 255, 0)
#     }
#     for i, (X, Y, Z) in enumerate(axes)
# ]

# compas_rhino.xdraw_points(points, layer='test', clear_layer=False, redraw=True)
# compas_rhino.xdraw_lines(xlines, layer='test', clear_layer=False, redraw=True)
# compas_rhino.xdraw_lines(ylines, layer='test', clear_layer=False, redraw=True)

assembly = Assembly()

for block in blocks:
    # xyz = block.get_vertices_attributes('xyz')
    # xyz = transform(xyz, X)
    # for key, attr in block.vertices(True):
    #     attr['x'] = xyz[key][0]
    #     attr['y'] = xyz[key][1]
    #     attr['z'] = xyz[key][2]
    assembly.add_block(block)

data = {
    'assembly': assembly.to_data(),
    'blocks'  : {str(key): block.to_data() for key, block in assembly.blocks.items()}
}

with open(os.path.join(compas_rbe.DATA, 'shajay2.json'), 'w+') as f:
    json.dump(data, f)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass

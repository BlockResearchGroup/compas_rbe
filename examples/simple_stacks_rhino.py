from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import json

import compas
import compas_rhino
import compas_rbe

from compas.utilities import XFunc

from compas_rhino.artists import MeshArtist

from compas_rbe.assemblies import Block
from compas_rbe.assemblies import Assembly

# external functions

identify_interfaces = XFunc('compas_rbe.assemblies.identify_interfaces_xfunc', tmpdir=compas_rbe.TEMP)
compute_interface_forces = XFunc('compas_rbe.equilibrium.compute_interface_forces_xfunc', tmpdir=compas_rbe.TEMP)

# initialize BlockModel and list of blocks

assembly = Assembly()

# read block geometry data from json files

filepath = compas_rbe.get('simple_stack2.json')

with open(filepath, 'r') as fp:
    data = json.load(fp)
    for item in data:
        for fkey, cycle in item['face'].items():
            start = list(cycle.keys())[0]
            key = cycle[start]
            item['face'][fkey] = [start]
            while True:
                if key == start:
                    break
                item['face'][fkey].append(key)
                key = cycle[key]
        block = Block.from_data(item)
        assembly.add_block(block)

for key, attr in assembly.vertices(True):
    if assembly.blocks[key].attributes['name'] == 'Block_0':
        attr['is_support'] = True

# identify block interfaces and update block_model

data = {
    'assembly': assembly.to_data(),
    'blocks'  : {str(key): assembly.blocks[key].to_data() for key in assembly.blocks},
}

result = identify_interfaces(
    data,
    nmax=5,
    tmax=0.05,
    amin=0.01,
    lmin=0.01,
    face_face=True,
    face_edge=False,
    face_vertex=False
)

assembly.data = result['assembly']

for key in assembly.blocks:
    assembly.blocks[key].data = result['blocks'][str(key)]

# equilibrium

data = {
    'assembly': assembly.to_data(),
    'blocks'  : {str(key): assembly.blocks[key].to_data() for key in assembly.blocks},
}

result = compute_interface_forces(data)

assembly.data = result['assembly']

for key in assembly.blocks:
    assembly.blocks[key].data = result['blocks'][str(key)]

# blocks

artist = MeshArtist(None, layer='RBE::Blocks')
artist.clear_layer()

for key in assembly.blocks:
    block = assembly.blocks[key]
    block.name = "Block-{}".format(key)

    artist.mesh = block
    artist.draw_edges()

artist.redraw()

# interfaces

faces = []
for u, v, attr in assembly.edges(True):
    points = attr['interface_points'] + attr['interface_points'][0:1]

    faces.append({
        'points': points,
        'name'  : "{0}.interface.{1}-{2}".format(assembly.name, u, v),
        'color' : (255, 255, 255)
    })

compas_rhino.xdraw_faces(faces, layer="RBE::Interfaces", clear=True, redraw=True)

# forces

scale = 0.11
eps   = 1e-3

lines = []
for a, b, attr in assembly.edges(True):

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
                    'name'  : "{0}.force.{1}-{2}.{3}".format(assembly.name, a, b, i),
                    'arrow' : 'end'
                })

            if scale * c_nn > eps:
                # tension force
                lines.append({
                    'start' : sp,
                    'end'   : [sp[axis] - scale * c_nn * w[axis] for axis in range(3)],
                    'color' : (255, 0, 0),
                    'name'  : "{0}.force.{1}-{2}.{3}".format(assembly.name, a, b, i),
                    'arrow' : 'end'
                })

compas_rhino.xdraw_lines(lines, layer="RBE::Forces", clear=True, redraw=True)



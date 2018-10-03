from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import json

import compas
import compas_rhino
import compas_rbe

from compas_rhino.utilities import XFunc

from compas_rbe.assemblies import Block
from compas_rbe.assemblies import Assembly

from compas_rbe.rhino import AssemblyArtist


# ==============================================================================
# external functions
# ==============================================================================

identify_interfaces = XFunc('compas_rbe.assemblies.identify_interfaces_xfunc')
identify_interfaces.tmpdir = compas_rbe.TEMP

compute_interface_forces = XFunc('compas_rbe.equilibrium.compute_interface_forces_xfunc')
compute_interface_forces.tmpdir = compas_rbe.TEMP

# for rhinomac

identify_interfaces.paths  = [compas_rbe.SRC]
compute_interface_forces.paths  = [compas_rbe.SRC]

# update this

mypython = "/Users/vanmelet/anaconda3/bin/python"

identify_interfaces.python = mypython
compute_interface_forces.python = mypython


# ==============================================================================
# initialise assembly from stored block data
# ==============================================================================

assembly = Assembly()

# read block geometry data from sample json file

filepath = compas_rbe.get('simple_stack2.json')

with open(filepath, 'r') as fp:
    data = json.load(fp)

    for item in data:

        # simple_stack2.json still uses a dict of half-edges to represent a face
        # instead of simple lists
        for fkey, cycle in item['face'].items():
            start = list(cycle.keys())[0]
            key = cycle[start]
            item['face'][fkey] = [start]
            while True:
                if key == start:
                    break
                item['face'][fkey].append(key)
                key = cycle[key]

        assembly.add_block(Block.from_data(item))

# mark the first block as support
# this will keep it fixed and allow it to provide reaction forces

for key, attr in assembly.vertices(True):
    if assembly.blocks[key].attributes['name'] == 'Block_0':
        attr['is_support'] = True


# ==============================================================================
# identify block interfaces
# ==============================================================================

# convert all data to built-in python types to simplify serialisation

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

# update assembly and blocks

assembly.data = result['assembly']

for key in assembly.blocks:
    assembly.blocks[key].data = result['blocks'][str(key)]


# ==============================================================================
# compute equilibrium
# ==============================================================================

data = {
    'assembly': assembly.to_data(),
    'blocks'  : {str(key): assembly.blocks[key].to_data() for key in assembly.blocks},
}

result = compute_interface_forces(data)

# update assembly and blocks

assembly.data = result['assembly']

for key in assembly.blocks:
    assembly.blocks[key].data = result['blocks'][str(key)]


# ==============================================================================
# draw result
# ==============================================================================

artist = AssemblyArtist(assembly, layer='RBE')
artist.clear_layer()

artist.draw_blocks()
artist.draw_interfaces()
artist.draw_forces()

artist.redraw()

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas
import compas_rbe

from compas_rhino.utilities import XFunc

from compas_rbe.datastructures import Assembly
from compas_rbe.rhino import AssemblyArtist


identify_interfaces = XFunc('compas_rbe.interfaces.identify_interfaces_xfunc', tmpdir=compas_rbe.TEMP)
compute_iforces = XFunc('compas_rbe.equilibrium.compute_iforces_xfunc', tmpdir=compas_rbe.TEMP)

identify_interfaces.python = '/Users/vanmelet/anaconda3/bin/python3'
compute_iforces.python = '/Users/vanmelet/anaconda3/bin/python3'

identify_interfaces.paths = ['/Users/vanmelet/Code/BlockResearchGroup/compas_rbe/src']
compute_iforces.paths = ['/Users/vanmelet/Code/BlockResearchGroup/compas_rbe/src']


# initialize assembly and blocks from json file

assembly = Assembly.from_json(compas_rbe.get('genevault.json'))

# identify block interfaces and update block_model

data = {
    'assembly': assembly.to_data(),
    'blocks'  : {str(key): assembly.blocks[key].to_data() for key in assembly.blocks},
}

result = identify_interfaces(data, nmax=10, tmax=0.05, amin=0.01, lmin=0.01)

assembly.data = result['assembly']

for key in assembly.blocks:
    assembly.blocks[key].data = result['blocks'][str(key)]

# equilibrium

data = {
    'assembly': assembly.to_data(),
    'blocks'  : {str(key): assembly.blocks[key].to_data() for key in assembly.blocks},
}

result = compute_iforces(data, solver='CPLEX')

assembly.data = result['assembly']

for key in assembly.blocks:
    assembly.blocks[key].data = result['blocks'][str(key)]

# result

artist = AssemblyArtist(assembly, layer='RBE')

artist.clear_layer()
artist.draw_blocks()
artist.draw_interfaces()
artist.draw_selfweight(scale=0.25)
artist.draw_forces(scale=0.25)

# check

total_selfweight = sum(assembly.blocks[key].volume() for key in assembly.vertices_where({'is_support': True}))

total_support = 0

# for a, b, attr in assembly.edges(True):
#     if assembly.vertex[a]['is_support']:
#         for i in range(len(attr['interface_points'])):
#             c_np = attr['interface_forces'][i]['c_np']
#             total_support += c_np

#     elif assembly.vertex[b]['is_support']:
#         for i in range(len(attr['interface_points'])):
#             c_np = attr['interface_forces'][i]['c_np']
#             total_support += c_np

#     else:
#         pass


print(total_support)
print(total_selfweight)
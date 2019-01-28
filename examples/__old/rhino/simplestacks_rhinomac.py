from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas
import compas_rbe

from compas_rhino.utilities import XFunc

from compas_rbe.datastructures import Assembly
from compas_rbe.rhino import AssemblyArtist


# replace this by RPC server
assembly_interfaces_ = XFunc('compas_rbe.interfaces.assembly_interfaces_xfunc', tmpdir=compas_rbe.TEMP)
compute_interface_forces_ = XFunc('compas_rbe.equilibrium.compute_interface_forces_xfunc', tmpdir=compas_rbe.TEMP)

# replace this by automated search for python executables
# based on .(bash_)profile
assembly_interfaces_.python = '/Users/vanmelet/anaconda3/bin/python3'
compute_interface_forces_.python = '/Users/vanmelet/anaconda3/bin/python3'

# replace 
assembly_interfaces_.paths = ['/Users/vanmelet/Code/BlockResearchGroup/compas_rbe/src']
compute_interface_forces_.paths = ['/Users/vanmelet/Code/BlockResearchGroup/compas_rbe/src']


# wrapper
def assembly_interfaces(assembly, nmax=10, tmax=0.05, amin=0.01, lmin=0.01):
    data = {'assembly': assembly.to_data(),
            'blocks'  : {str(key): assembly.blocks[key].to_data() for key in assembly.blocks}}
    result = assembly_interfaces_(data, nmax=nmax, tmax=tmax, amin=amin, lmin=lmin)
    assembly.data = result['assembly']
    for key in assembly.blocks:
        assembly.blocks[key].data = result['blocks'][str(key)]


#wrapper
def compute_interface_forces(assembly, solver='CPLEX'):
    data = {'assembly': assembly.to_data(),
            'blocks'  : {str(key): assembly.blocks[key].to_data() for key in assembly.blocks},}
    result = compute_interface_forces_(data, solver=solver)
    assembly.data = result['assembly']
    for key in assembly.blocks:
        assembly.blocks[key].data = result['blocks'][str(key)]


# initialize assembly and blocks from json file
assembly = Assembly.from_json(compas_rbe.get('simple_stack_1.json'))

# identify block interfaces and update block_model
assembly_interfaces(assembly)

# equilibrium
compute_interface_forces(assembly)

# result
artist = AssemblyArtist(assembly, layer='RBE')
artist.clear_layer()
artist.draw_blocks()
artist.draw_interfaces()
artist.draw_selfweight(scale=0.25)
artist.draw_forces(scale=0.25)
artist.redraw()

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
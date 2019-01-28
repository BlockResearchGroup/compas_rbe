from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas
import compas_rbe

from compas.utilities import XFunc

from compas_rbe.datastructures import Assembly

from compas_rbe.rhino import AssemblyArtist
from compas_rbe.rhino import AssemblyHelper


assembly_interfaces = XFunc('compas_rbe.interfaces.assembly_interfaces_xfunc', tmpdir=compas_rbe.TEMP)
compute_interface_forces = XFunc('compas_rbe.equilibrium.compute_interface_forces_xfunc', tmpdir=compas_rbe.TEMP)


# initialize assembly and blocks from json file

assembly = Assembly.from_json(compas_rbe.get('simple_stack_4.json'))

# identify block interfaces and update block_model

data = {
    'assembly': assembly.to_data(),
    'blocks'  : {str(key): assembly.blocks[key].to_data() for key in assembly.blocks},
}

result = assembly_interfaces(data, nmax=10, tmax=0.05, amin=0.01, lmin=0.01)

assembly.data = result['assembly']

for key in assembly.blocks:
    assembly.blocks[key].data = result['blocks'][str(key)]

assembly.draw('RBE')

# equilibrium

data = {
    'assembly': assembly.to_data(),
    'blocks'  : {str(key): assembly.blocks[key].to_data() for key in assembly.blocks},
}

result = compute_interface_forces(data, solver='ECOS')

assembly.data = result['assembly']

for key in assembly.blocks:
    assembly.blocks[key].data = result['blocks'][str(key)]

assembly.draw('RBE')

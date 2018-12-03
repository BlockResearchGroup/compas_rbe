from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas
import compas_rbe

from compas_rbe.datastructures import Assembly

from compas_rbe.interfaces import identify_interfaces
from compas_rbe.equilibrium import compute_interfaceforces

from compas_rbe.viewer import AssemblyViewer


# initialize assembly and blocks from json file

assembly = Assembly.from_json(compas_rbe.get('simplestack.json'))

# identify block interfaces and update block_model

identify_interfaces(
    assembly,
    nmax=5,
    tmax=0.05,
    amin=0.01,
    lmin=0.01,
)

# equilibrium

compute_interfaceforces(assembly, verbose=True, solver='CVXOPT')

# result

viewer = AssemblyViewer()
viewer.assembly = assembly
viewer.show()

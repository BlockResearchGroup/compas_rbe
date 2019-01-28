from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas
import compas_rbe

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import assembly_interfaces
from compas_assembly.viewer import AssemblyViewer

from compas_rbe.equilibrium import compute_interface_forces_cvx


# initialize assembly and blocks from json file

assembly = Assembly.from_json(compas_rbe.get('genevault.json'))

# identify block interfaces and update block_model

assembly_interfaces(
    assembly,
    nmax=10,
    tmax=0.05,
    amin=0.01,
    lmin=0.01,
)

# equilibrium

# compute_interface_forces_cvx(assembly, verbose=True)

# result

viewer = AssemblyViewer()
viewer.assembly = assembly
viewer.show()

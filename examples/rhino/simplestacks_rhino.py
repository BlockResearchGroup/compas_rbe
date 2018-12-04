from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas
import compas_rbe

from compas.utilities import XFunc

from compas_rbe.datastructures import Assembly

from compas_rbe.rhino import AssemblyArtist
from compas_rbe.rhino import AssemblyHelper


# initialize assembly and blocks from json file

assembly = Assembly.from_json(compas_rbe.get('curve_components.json'))

print(list(assembly.vertices_where({'is_support': True})))

# identify block interfaces and update block_model

# identify_interfaces(
#     assembly,
#     nmax=10,
#     tmax=0.05,
#     amin=0.01,
#     lmin=0.01,
# )

# equilibrium

# compute_iforces(assembly, solver='CPLEX', verbose=True)

# result

viewer = AssemblyViewer()
viewer.assembly = assembly
viewer.show()

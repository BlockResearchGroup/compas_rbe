from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas

from compas.datastructures import mesh_transform
from compas.geometry import Translation

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import Block
from compas_assembly.datastructures import assembly_interfaces
from compas_assembly.viewer import AssemblyViewer

from compas_rbe.equilibrium import compute_interface_forces_cvx


assembly = Assembly()

b1 = Block.from_polyhedron(6)
b2 = Block.from_polyhedron(6)

u, v = list(b1.edges())[0]

l = b1.edge_length(u, v)

T1 = Translation([0, 0, -0.5 * l])
T2 = Translation([0, 0, +0.5 * l])

mesh_transform(b1, T1)
mesh_transform(b2, T2)

assembly.add_block(b1, is_support=True)
assembly.add_block(b2)


# identify block interfaces and update block_model

assembly_interfaces(
    assembly,
    nmax=10,
    tmax=0.05,
    amin=0.01,
    lmin=0.01,
)

# equilibrium

compute_interface_forces_cvx(assembly, solver='CPLEX', verbose=True)

# result

# assembly.to_json(compas_rbe.get('{}_result.json'.format(stack)))

# for a, b, attr in assembly.edges(True):
#     if attr['interface_forces']:
#         w = attr['interface_uvw'][2]

#         print(len(attr['interface_points']))
#         print(len(attr['interface_forces']))

#         for i in range(len(attr['interface_points'])):
#             sp   = attr['interface_points'][i]
#             c_np = attr['interface_forces'][i]['c_np']
#             c_nn = attr['interface_forces'][i]['c_nn']

#             print(c_np)
#             print(c_nn)


viewer = AssemblyViewer()
viewer.assembly = assembly
viewer.show()

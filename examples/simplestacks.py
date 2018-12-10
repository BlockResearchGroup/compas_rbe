from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas
import compas_rbe

from compas_rbe.datastructures import Assembly

from compas_rbe.interfaces import identify_interfaces
from compas_rbe.equilibrium import compute_iforces_cvx as compute_iforces

from compas_rbe.viewer import AssemblyViewer


stack = 'simple_stack_rotate'

# initialize assembly and blocks from json file

assembly = Assembly.from_json(compas_rbe.get('{}.json'.format(stack)))

print(list(assembly.vertices_where({'is_support': True})))

# identify block interfaces and update block_model

identify_interfaces(
    assembly,
    nmax=10,
    tmax=0.05,
    amin=0.01,
    lmin=0.01,
)

# equilibrium

compute_iforces(assembly, solver='CPLEX', verbose=True)

# result

assembly.to_json(compas_rbe.get('{}_result.json'.format(stack)))

for a, b, attr in assembly.edges(True):
    if attr['interface_forces']:
        w = attr['interface_uvw'][2]

        print(len(attr['interface_points']))
        print(len(attr['interface_forces']))

        for i in range(len(attr['interface_points'])):
            sp   = attr['interface_points'][i]
            c_np = attr['interface_forces'][i]['c_np']
            c_nn = attr['interface_forces'][i]['c_nn']

            print(c_np)
            print(c_nn)

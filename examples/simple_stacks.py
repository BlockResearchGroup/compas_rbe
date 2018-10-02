from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import json

import compas_rbe

from compas_rbe.assemblies import Block
from compas_rbe.assemblies import Assembly
from compas_rbe.assemblies import identify_interfaces

from compas_rbe.equilibrium import compute_interface_forces


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

identify_interfaces(
    assembly,
    nmax=5,
    tmax=0.05,
    amin=0.01,
    lmin=0.01,
)

# equilibrium

compute_interface_forces(assembly, verbose=True)

# result

print(assembly)

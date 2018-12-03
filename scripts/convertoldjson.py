from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import json

from compas_rbe.datastructures import Block
from compas_rbe.datastructures import Assembly


def convert(source, destination):

    assembly = Assembly()

    with open(source, 'r') as fo:
        data = json.load(fo)
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

    assembly.to_json(destination)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import compas
    import compas_rbe

    convert(compas_rbe.get('simple_stack.json'), compas_rbe.get('simplestack.json'))

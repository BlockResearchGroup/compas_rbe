from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
import sys
import json

import compas
import compas_rbe

from compas_rbe.rbe import Assembly
from compas_rbe.rbe import Block


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = []


def cycle(d):
    start = next(iter(d))
    key = start
    keys = [key]
    while True:
        key = d[key]
        if key == start:
            break
        keys.append(key)
    return keys


with open(os.path.join(compas_rbe.TEMP, 'cctv_blocks.json'), 'r') as f:
    blocks = json.load(f)

with open(os.path.join(compas_rbe.TEMP, 'cctv_support.json'), 'r') as f:
    supports = json.load(f)

assembly = Assembly()

for data in blocks:
    face = {}
    for fkey in data[0]['face']:
        keys = cycle(data[0]['face'][fkey])
        face[fkey] = keys
    data[0]['face'] = face
    block = Block.from_data(data[0])
    for key, attr in block.vertices(True):
        attr['x'] *= 0.01
        attr['y'] *= 0.01
        attr['z'] *= 0.01
    assembly.add_block(block)

for data in supports:
    face = {}
    for fkey in data[0]['face']:
        keys = cycle(data[0]['face'][fkey])
        face[fkey] = keys
    data[0]['face'] = face
    block = Block.from_data(data[0])
    for key, attr in block.vertices(True):
        attr['x'] *= 0.01
        attr['y'] *= 0.01
        attr['z'] *= 0.01
    assembly.add_block(block, is_support=True)

data = {
    'assembly': assembly.to_data(),
    'blocks'  : {str(key): block.to_data() for key, block in assembly.blocks.items()}
}

with open(os.path.join(compas_rbe.DATA, 'cctv.json'), 'w+') as f:
    json.dump(data, f)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass

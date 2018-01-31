from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
import json

import compas
import compas_rhino
import compas_rbe

from compas_rbe.cad.rhino import Assembly


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


guids = compas_rhino.select_surfaces()
names = compas_rhino.get_object_names(guids)

assembly = Assembly.from_polysurfaces(guids)

with open(os.path.join(compas_rbe.DATA, 'simple_stack2.json'), 'w+') as fp:
    data = []
    i = 0
    for block in assembly.blocks.values():
        block.attributes['name'] = names[i]
        data.append(block.to_data())
        i += 1
    json.dump(data, fp)

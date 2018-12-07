from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas
import compas_rbe

from compas_rbe.datastructures import Assembly

from compas_rbe.rhino import AssemblyArtist
from compas_rbe.rhino import AssemblyHelper


assembly = Assembly.from_json(compas_rbe.get('simple_stack_4_result.json'))

artist = AssemblyArtist(assembly, layer='RBE')

artist.clear_layer()
artist.draw_blocks()
artist.draw_interfaces()
artist.draw_forces()

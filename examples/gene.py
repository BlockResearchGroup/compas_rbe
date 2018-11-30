from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import json

import compas
import compas_rhino
import compas_rbe

from compas_rhino.utilities import XFunc

from compas_rbe.datastructures import Block
from compas_rbe.datastructures import Assembly

from compas_rbe.rhino import AssemblyArtist


guids = compas_rhino.select_meshes()

assembly = Assembly.from_meshes(guids)

print(assembly)


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
from compas_rbe.rhino import AssemblyHelper


# ==============================================================================
# external functions
# ==============================================================================

identify_interfaces = XFunc('compas_rbe.datastructures.identify_interfaces_xfunc')
identify_interfaces.tmpdir = compas_rbe.TEMP

compute_interface_forces = XFunc('compas_rbe.equilibrium.compute_interface_forces_xfunc')
compute_interface_forces.tmpdir = compas_rbe.TEMP


# ==============================================================================
# make an artist
# ==============================================================================

artist = AssemblyArtist(None, layer='RBE')
artist.clear_layer()


# ==============================================================================
# initialise assembly from Rhino geometry
# ==============================================================================

guids = compas_rhino.select_meshes()
assembly = Assembly.from_meshes(guids)

artist.assembly = assembly

# ==============================================================================
# draw blocks
# ==============================================================================

artist.draw_blocks()
artist.draw_vertices(color={key: '#ff0000' for key in assembly.vertices_where({'is_support': True})})

artist.redraw()


# ==============================================================================
# identify support
# ==============================================================================

# key = AssemblyHelper.select_vertices(assembly, "Select the vertex representing the support block.")

# if key is not None:
#     assembly.set_vertex_attribute(key, 'is_support', True)


# ==============================================================================
# draw blocks
# ==============================================================================

artist.clear_vertices()
artist.draw_vertices(color={key: '#ff0000' for key in assembly.vertices_where({'is_support': True})})

artist.redraw()


# ==============================================================================
# identify block interfaces
# ==============================================================================

# convert all data to built-in python types to simplify serialisation

data = {
    'assembly': assembly.to_data(),
    'blocks'  : {str(key): assembly.blocks[key].to_data() for key in assembly.blocks},
}

result = identify_interfaces(
    data,
    nmax=10,
    tmax=0.05,
    amin=0.01,
    lmin=0.01,
    face_face=True,
    face_edge=False,
    face_vertex=False
)

# update assembly and blocks

assembly.data = result['assembly']

for key in assembly.blocks:
    assembly.blocks[key].data = result['blocks'][str(key)]


# ==============================================================================
# draw interfaces
# ==============================================================================

artist.draw_edges()
artist.draw_interfaces()

artist.redraw()


# ==============================================================================
# compute equilibrium
# ==============================================================================

data = {
    'assembly': assembly.to_data(),
    'blocks'  : {str(key): assembly.blocks[key].to_data() for key in assembly.blocks},
}

result = compute_interface_forces(data)

# update assembly and blocks

assembly.data = result['assembly']

for key in assembly.blocks:
    assembly.blocks[key].data = result['blocks'][str(key)]


# ==============================================================================
# draw forces
# ==============================================================================

# artist.draw_forces()
artist.color_interfaces()

artist.redraw()

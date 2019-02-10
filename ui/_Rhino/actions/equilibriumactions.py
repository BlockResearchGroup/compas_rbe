from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os

import compas
import compas_rhino
import compas_rbe

from compas.utilities import XFunc

from compas_rbe.rhino import AssemblyArtist

HERE = os.path.abspath(os.path.dirname(__file__))

try:
    import rhinoscriptsyntax as rs
except ImportError:
    pass

compute_interface_forces = XFunc('compas_rbe.equilibrium.compute_interface_forces_xfunc', tmpdir=compas_rbe.TEMP)


__all__ = ['EquilibriumActions']


class EquilibriumActions(object):

    def compute_interface_forces(self):
        assembly = self.assembly

        data = {
            'assembly': assembly.to_data(),
            'blocks'  : {str(key): assembly.blocks[key].to_data() for key in assembly.blocks},
        }

        result = compute_interface_forces(data, solver='ECOS')

        assembly.data = result['assembly']

        for key in assembly.blocks:
            assembly.blocks[key].data = result['blocks'][str(key)]

        assembly.draw(self.settings['layer'])

        artist = AssemblyArtist(assembly, layer=self.settings['layer'])
        artist.draw_forces()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass

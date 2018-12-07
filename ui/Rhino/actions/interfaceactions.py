from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os

import compas
import compas_rhino
import compas_rbe

from compas.utilities import XFunc

HERE = os.path.abspath(os.path.dirname(__file__))

try:
    import rhinoscriptsyntax as rs
except ImportError:
    pass


identify_interfaces = XFunc('compas_rbe.interfaces.identify_interfaces_xfunc', tmpdir=compas_rbe.TEMP)


__all__ = ['InterfaceActions']


class InterfaceActions(object):

    def identify_interfaces(self):
        assembly = self.assembly

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

        assembly.data = result['assembly']

        for key in assembly.blocks:
            assembly.blocks[key].data = result['blocks'][str(key)]

        assembly.draw(self.settings['layer'])

    def planarize_interfaces(self):
        pass


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass

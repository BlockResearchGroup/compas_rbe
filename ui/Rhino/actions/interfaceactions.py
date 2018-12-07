from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os

import compas
import compas_rhino
import compas_rbe

# from compas_rbe.interfaces import identify_interfaces_xfunc

HERE = os.path.abspath(os.path.dirname(__file__))

try:
    import rhinoscriptsyntax as rs
except ImportError:
    pass


__all__ = ['InterfaceActions']


class InterfaceActions(object):

    def identify_interfaces(self):
        pass

    def planarize_interfaces(self):
        pass


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass

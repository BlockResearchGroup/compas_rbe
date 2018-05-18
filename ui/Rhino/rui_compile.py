from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = []


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from compas_rhino.ui.rui import compile_rui
    from rui_controller import DEAMacroController

    compile_rui(DEAMacroController, 'rui_controller', rui_config='rui_config.json')

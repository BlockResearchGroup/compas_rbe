from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
import json

import compas
import compas_rhino
import compas_rbe

from compas.utilities import now

from compas_rbe.datastructures import Assembly

from compas_rbe.rhino import AssemblyArtist

from actions import AssemblyActions
from actions import BlockActions
from actions import InterfaceActions
from actions import EquilibriumActions

HERE = os.path.abspath(os.path.dirname(__file__))

try:
    import rhinoscriptsyntax as rs
except ImportError:
    pass


__all__ = ['RBEFrontController']


class RBEFrontController(EquilibriumActions,
                         InterfaceActions,
                         BlockActions,
                         AssemblyActions):

    instancename = 'rbe'

    def __init__(self):
        self.assembly = None
        self.settings = {
            'current_working_directory' : None,
        }

    @property
    def cwd(self):
        cwd = self.settings['current_working_directory']
        if not cwd or not os.path.exists(cwd):
            cwd = HERE
        return cwd

    @cwd.setter
    def cwd(self, path):
        self.settings['current_working_directory'] = path

    def init(self):
        compas_rhino.clear_layers([self.settings['form.layer'], self.settings['force.layer']])

    def update_settings(self):
        compas_rhino.update_settings(self.settings)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass

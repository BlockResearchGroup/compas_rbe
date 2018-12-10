from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


import os
import sys

import rhinoscriptsyntax as rs
import scriptcontext as sc

import Rhino

import compas_rbe

from compas_rbe.rhino import UpdateSettingsForm


__commandname__ = "RBE_settings"


def RunCommand(is_interactive):
    if not 'RBE' in sc.sticky:
        raise Exception('Initialise RBE first!')

    RBE = sc.sticky['RBE']

    try:

        dialog = UpdateSettingsForm(RBE['settings'])
        
        if dialog.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow):
            RBE['settings'].update(dialog.settings)

    except Exception as error:

        print(error)

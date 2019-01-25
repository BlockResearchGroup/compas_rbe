from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


import traceback
import scriptcontext as sc
import Rhino

from compas_rhino.etoforms import SettingsForm


__commandname__ = "RBE_settings"


def RunCommand(is_interactive):
    try:
        if 'RBE' not in sc.sticky:
            raise Exception('Initialise RBE first!')

        RBE = sc.sticky['RBE']

        dialog = SettingsForm(RBE['settings'])

        if dialog.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow):
            RBE['settings'].update(dialog.settings)

            assembly = RBE['assembly']
            if assembly:
                assembly.draw(RBE['settings'])

    except Exception as error:
        print(error)
        print(traceback.format_exc())


if __name__ == '__main__':

    RunCommand(True)

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from ast import literal_eval

import scriptcontext as sc
import traceback

import Rhino.UI

import compas_rhino

from compas_rbe.rhino import AssemblyHelper
from compas_rbe.rhino import PropertyListForm


__commandname__ = "RBE_assembly_update_vertex_attributes"


def update_vertex_attributes(assembly, keys, names=None):
    if not names:
        names = assembly.default_vertex_attributes.keys()
    names = sorted(names)
    values = [assembly.vertex[keys[0]][name] for name in names]
    if len(keys) > 1:
        for i, name in enumerate(names):
            for key in keys[1:]:
                if values[i] != assembly.vertex[key][name]:
                    values[i] = '-'
                    break
    values = map(str, values)

    dialog = PropertyListForm(names, values)
    if dialog.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow):
        values = dialog.values
    else:
        values = None

    if values:
        for name, value in zip(names, values):
            if value != '-':
                for key in keys:
                    try:
                        assembly.vertex[key][name] = literal_eval(value)
                    except (ValueError, TypeError):
                        assembly.vertex[key][name] = value
        return True
    return False


def RunCommand(is_interactive):
    try:
        if 'RBE' not in sc.sticky:
            raise Exception('Initialise RBE first!')

        RBE = sc.sticky['RBE']

        assembly = RBE['assembly']

        keys = AssemblyHelper.select_vertices(assembly)
        if not keys:
            return

        if update_vertex_attributes(assembly, keys):
            assembly.draw(RBE['settings'])

    except Exception as error:
        print(error)
        print(traceback.format_exc())


if __name__ == '__main__':

    RunCommand(True)

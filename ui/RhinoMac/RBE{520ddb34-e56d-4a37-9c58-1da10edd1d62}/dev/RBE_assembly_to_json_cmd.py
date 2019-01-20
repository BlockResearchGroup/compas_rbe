from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import rhinoscriptcontext as rs
import scriptcontext as sc
import traceback
import os

import compas_rhino
import compas_rbe


__commandname__ = "RBE_assembly_to_json"


def RunCommand(is_interactive):
    try:
        if 'RBE' not in sc.sticky:
            raise Exception('Initialise RBE first!')

        RBE = sc.sticky['RBE']

        folder = compas_rhino.select_folder(default=compas_rbe.DATA)
        if not folder:
            return

        filename = rs.GetString('Name of the json file?')
        if not filename:
            return

        name, ext = os.path.splitext(filename)
        if ext != '.json':
            filename = name + ext + '.json'

        assembly = RBE['assembly']
        assembly.to_json(os.path.join(folder, filename))

    except Exception as error:
        print(error)
        print(traceback.format_exc())


if __name__ == '__main__':

    RunCommand(True)

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


import rhinoscriptsyntax as rs
import scriptcontext as sc

import Rhino

import os
import sys
import traceback

import compas_rhino
import compas_rbe

from compas_rbe.datastructures import Assembly


__commandname__ = "RBE_assembly_from_json"


def RunCommand(is_interactive):
    try:
        if 'RBE' not in sc.sticky:
            raise Exception('Initialise RBE first!')

        RBE = sc.sticky['RBE']

        path = compas_rhino.select_file(folder=compas_rbe.DATA, filter='JSON files (*.json)|*.json||')
        if not path:
            return

        RBE['assembly'] = assembly = Assembly.from_json(path)

        assembly.draw(RBE['settings'])

    except Exception as error:
        print(error)
        print(traceback.format_exc())


if __name__ == '__main__':

    RunCommand(True)

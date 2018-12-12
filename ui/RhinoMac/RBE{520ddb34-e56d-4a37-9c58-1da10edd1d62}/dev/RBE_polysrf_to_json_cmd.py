from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
import sys

import rhinoscriptsyntax as rs
import scriptcontext as sc

import Rhino

import compas
import compas_rhino
import compas_rbe
from compas_rbe.datastructures import Assembly

__commandname__ = "RBE_polysrf_to_json"


def RunCommand(is_interactive):
    try:

        if not 'RBE' in sc.sticky:
            raise Exception('Initialise RBE first!')

        RBE = sc.sticky['RBE']

        assembly = Assembly()

        guids = compas_rhino.select_surfaces()
        my_assembly = assembly.add_blocks_from_polysurfaces(guids)

        filename = rs.SaveFileName(
            "Save",
            filter='JSON files (*.json)|*.json||',
            folder=compas_rbe.DATA)

        assembly.to_json(filename)

    except Exception as error:

        print(error)

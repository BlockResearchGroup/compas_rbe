from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


import rhinoscriptsyntax as rs
import scriptcontext as sc

import Rhino

import os
import sys

import compas_rhino
import compas_rbe

from compas_rbe.datastructures import Assembly
from compas_rbr.rhino import AssemblyHelper


__commandname__ = "RBE_assembly_update_vertex_attributes"


def RunCommand(is_interactive):
    if not 'RBE' in sc.sticky:
        raise Exception('Initialise RBE first!')

    RBE = sc.sticky['RBE']

    try:
        assembly = RBE['assembly']
        
        keys = AssemblyHelper.select_vertices(assembly)
        if not keys:
            return

        if AssemblyHelper.update_vertex_attributes(assembly, keys):
            assembly.draw(RBE['settings']['layer'])

    except Exception as error:

        print(error)

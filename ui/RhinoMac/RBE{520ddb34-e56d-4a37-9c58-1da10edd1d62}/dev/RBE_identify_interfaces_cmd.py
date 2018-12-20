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

from compas_rhino.utilities import XFunc

from compas_rbe.datastructures import Assembly

identify_interfaces_ = XFunc(
    'compas_rbe.interfaces.identify_interfaces_xfunc', tmpdir=compas_rbe.TEMP)

identify_interfaces_.paths = [compas_rbe.SRC]


def identify_interfaces(assembly, nmax=10, tmax=0.05, amin=0.01, lmin=0.01):
    data = {
        'assembly': assembly.to_data(),
        'blocks':
        {str(key): assembly.blocks[key].to_data()
         for key in assembly.blocks}
    }
    result = identify_interfaces_(
        data, nmax=nmax, tmax=tmax, amin=amin, lmin=lmin)
    assembly.data = result['assembly']
    for key in assembly.blocks:
        assembly.blocks[key].data = result['blocks'][str(key)]


__commandname__ = "RBE_identify_interfaces"


def RunCommand(is_interactive):
    try:

        if not 'RBE' in sc.sticky:
            raise Exception('Initialise RBE first!')

        RBE = sc.sticky['RBE']

        identify_interfaces_.python = RBE['settings']['pythonpath']

        assembly = RBE['assembly']

        identify_interfaces(assembly)

        assembly.draw(RBE['settings'])

    except Exception as error:

        print(error)
        print(traceback.format_exc())

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

from compas_rhino.utilities import XFunc

from compas_rbe.datastructures import Assembly
from compas_rbe.rhino import AssemblyArtist


compute_iforces_ = XFunc('compas_rbe.equilibrium.compute_iforces_xfunc', tmpdir=compas_rbe.TEMP)
compute_iforces_.python = '/Users/vanmelet/anaconda3/bin/python3'
compute_iforces_.paths = ['/Users/vanmelet/Code/BlockResearchGroup/compas_rbe/src']


def compute_iforces(assembly, solver='CPLEX'):
    data = {'assembly': assembly.to_data(),
            'blocks'  : {str(key): assembly.blocks[key].to_data() for key in assembly.blocks},}
    result = compute_iforces_(data, solver=solver)
    assembly.data = result['assembly']
    for key in assembly.blocks:
        assembly.blocks[key].data = result['blocks'][str(key)]


__commandname__ = "RBE_compute_iforces"


def RunCommand(is_interactive):
    if not 'RBE' in sc.sticky:
        raise Exception('Initialise RBE first!')
    RBE = sc.sticky['RBE']

    try:

        assembly = RBE['assembly']

        compute_iforces(assembly)

        artist = AssemblyArtist(assembly, layer=RBE['settings']['layer'])
        artist.clear_layer()
        artist.draw_blocks()
        artist.draw_interfaces()
        artist.draw_selfweight(scale=0.25)
        artist.draw_forces(scale=0.25)
        artist.redraw()

    except Exception as error:

        print(error)

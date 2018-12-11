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

identify_interfaces_ = XFunc(
    'compas_rbe.interfaces.identify_interfaces_xfunc', tmpdir=compas_rbe.TEMP)

identify_interfaces_.python = '/Users/kaot/anaconda3/envs/rbe/bin/python'
identify_interfaces_.paths = ['/Users/kaot/compas-dev/compas_rbe/src']

compute_iforces_ = XFunc(
    'compas_rbe.equilibrium.compute_iforces_xfunc', tmpdir=compas_rbe.TEMP)
compute_iforces_.python = '/Users/kaot/anaconda3/envs/rbe/bin/python'
compute_iforces_.paths = ['/Users/kaot/compas-dev/compas_rbe/src']


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


def compute_iforces(assembly, solver='CPLEX'):
    data = {
        'assembly': assembly.to_data(),
        'blocks':
        {str(key): assembly.blocks[key].to_data()
         for key in assembly.blocks},
    }
    result = compute_iforces_(data, solver=solver)
    assembly.data = result['assembly']
    for key in assembly.blocks:
        assembly.blocks[key].data = result['blocks'][str(key)]


__commandname__ = "RBE_compute_interfces_and_forces"  # => the part before _cmd.py


def RunCommand(is_interactive):
    RBE = {
        'settings': {
            'layer': 'RBE',
        },
        'assembly': None,
    }

    compas_rhino.clear_layer(RBE['settings']['layer'])
    sc.sticky['RBE'] = RBE

    print('Success!')

    path = compas_rhino.select_file(
        folder=compas_rbe.DATA, filter='JSON files (*.json)|*.json||')

    if not path:
        return

    RBE['assembly'] = assembly = Assembly.from_json(path)

    assembly.draw(RBE['settings']['layer'])

    # if not 'RBE' in sc.sticky:
    #     raise Exception('Initialise RBE first!')

    # RBE = sc.sticky['RBE']

    try:

        assembly = RBE['assembly']

        identify_interfaces(assembly)

        assembly.draw(RBE['settings']['layer'])

        compute_iforces(assembly)

        artist = AssemblyArtist(assembly, layer=RBE['settings']['layer'])
        artist.clear_layer()
        artist.draw_blocks()
        artist.draw_interfaces()
        artist.color_interfaces()
        artist.draw_selfweight(scale=0.1)
        artist.draw_forces(scale=0.1)
        artist.redraw()

    except Exception as error:

        print(error)

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

try:
    reload
except NameError:
    try:
        from importlib import reload
    except ImportError:
        from imp import reload

import rhinoscriptsyntax as rs
import scriptcontext as sc

import Rhino

import os
import sys
import traceback

import compas_rhino
import compas_rbe

from compas_rhino.utilities import XFunc

reload(compas_rbe.rhino.artists)
reload(compas_rbe.rhino)

from compas_rbe.datastructures import Assembly
from compas_rbe.rhino import AssemblyArtist

identify_interfaces_ = XFunc(
    'compas_rbe.interfaces.identify_interfaces_xfunc', tmpdir=compas_rbe.TEMP)
compute_iforces_ = XFunc(
    'compas_rbe.equilibrium.compute_iforces_xfunc', tmpdir=compas_rbe.TEMP)
identify_interfaces_.paths = compute_iforces_.paths = [compas_rbe.SRC]


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
    try:
        RBE = {
            'settings': {
                'layer': 'RBE',
                'pythonpath': '/Users/kaot/anaconda3/envs/rbe/bin/python',
                'scale.selfweight': 0.1,
                'scale.force': 0.1,
                'scale.friction': 0.1,
                'color.edge': (0, 0, 0),
                'color.vertex': (0, 0, 0),
                'color.vertex:is_support': (255, 0, 0),
                'eps.force': 1e-3,
                'eps.friction': 1e-3,
                'eps.selfweight': 1e-3,
                'show.vertices': True,
                'show.edges': True,
                'show.interfaces': True,
                'show.forces': True,
                'show.forces_as_vectors': True,
                'show.selfweight': True,
                'show.friction': True,
            },
            'assembly': None,
        }

        layer = RBE['settings']['layer']

        compas_rhino.clear_layer(RBE['settings']['layer'])
        sc.sticky['RBE'] = RBE

        identify_interfaces_.python = compute_iforces_.python = RBE[
            'settings']['pythonpath']

        print('Success!')

        path = compas_rhino.select_file(
            folder=compas_rbe.DATA, filter='JSON files (*.json)|*.json||')

        if not path:
            return

        RBE['assembly'] = assembly = Assembly.from_json(path)

        identify_interfaces(assembly)
        compute_iforces(assembly)

        assembly.draw(RBE['settings'])

    except Exception as error:

        print(error)
        print(traceback.format_exc())

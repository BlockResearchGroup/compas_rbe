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

# not sure if this will help
reload(compas_rbe)
# compas_rbe.relaod()

__commandname__ = "RBE_init"


def RunCommand(is_interactive):
    try:

        RBE = {
            'settings': {
                'layer': 'RBE',
                'pythonpath': '/Users/kaot/anaconda3/envs/rbe/bin/python',
                'scale.selfweight': 0.1,
                'scale.force': 0.1,
                'color.edge': (0, 0, 0),
                'color.vertex': (0, 0, 0),
                'color.vertex:is_support': (255, 0, 0),
                'eps.force': 1e-3,
                'eps.selfweight': 1e-3,
                'show.vertices': True,
                'show.edges': True,
                'show.interfaces': True,
                'show.forces': False,
                'show.selfweight': False,
                'show.friction': False,
            },
            'assembly': None,
        }

        compas_rhino.clear_layer(RBE['settings']['layer'])

        sc.sticky['RBE'] = RBE

        print('Success!')

    except Exception as error:

        print(error)
        print(traceback.format_exc())

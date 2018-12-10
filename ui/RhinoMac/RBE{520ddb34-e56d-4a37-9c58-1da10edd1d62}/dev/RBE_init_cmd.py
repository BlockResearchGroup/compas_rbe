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


__commandname__ = "RBE_init"


# add continuous saving as coroutine (asynchronous behaviour)
# use same principle as alternative approach to front controller on Rhino (Windows)
# possibly better cross-compatibility

# use sticky dict for temp saves
# init with init


def RunCommand(is_interactive):
    try:

        RBE = {
            'settings' : {
                'layer' : 'RBE',
            },
            'assembly' : None,
        }

        sc.sticky['RBE'] = RBE

        print('Success!')

    except Exception as error:

        print(error)

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
    # print(type(is_interactive), ':', is_interactive)
    try:

        RBE = {
            'settings' : {'layer' : 'RBE'},
            'assembly' : None,
        }

        sc.sticky['RBE'] = RBE

        # for path in os.environ:
        #     print(path)

        # print(sys.executable)

        # for path in sys.path:
        #     print(path)

        # print(sys.platform)
        # print(sys.version)
        # print(sys.version_info)

    except Exception as error:

        print(error)

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import importlib
import os
import sys

import compas_rhino

from compas._os import create_symlink
from compas._os import remove_symlink


HERE = os.path.abspath(os.path.dirname(__file__))
THERE = '/Users/vanmelet/Library/Application Support/McNeel/Rhinoceros/MacPlugIns/PythonPlugIns'


__all__ = []


def install():
    """Install compas_rbe for RhinoMac.

    Parameters
    ----------

    Examples
    --------
    .. code-block:: python

        pass

    """

    plugin_name = 'RBE{520ddb34-e56d-4a37-9c58-1da10edd1d62}'
    plugin_path = os.path.join(HERE, plugin_name)
    symlink_path = os.path.join(THERE, plugin_name)

    print('Installing PlugIn {} to RhinoMac PythonPlugIns.'.format(plugin_name))

    if os.path.exists(symlink_path):
        remove_symlink(symlink_path)

    create_symlink(plugin_path, symlink_path)

    print('OK: PlugIn {} Installed.'.format(plugin_name))


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass

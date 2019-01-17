from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import importlib
import os
import sys

from compas._os import create_symlink
from compas._os import remove_symlink


PLUGINS = 'Library/Application Support/McNeel/Rhinoceros/MacPlugIns/PythonPlugIns'

HOME = os.environ['HOME']
THERE = os.path.join(HOME, PLUGINS)


__all__ = []


def install(name, path):
    """Install compas_rbe for RhinoMac.

    Parameters
    ----------

    Examples
    --------
    .. code-block:: python

        pass

    """

    plugin_name = name
    plugin_path = os.path.join(os.path.abspath(path), plugin_name)

    devpath = os.path.join(plugin_path, 'dev')

    sys.path.insert(0, devpath)

    from __plugin__ import id as plugin_id

    symlink_path = os.path.join(THERE, "{}{}".format(plugin_name, plugin_id))

    print('Installing PlugIn {} to RhinoMac PythonPlugIns.'.format(plugin_name))

    if os.path.exists(symlink_path):
        remove_symlink(symlink_path)

    create_symlink(plugin_path, symlink_path)

    print('OK: PlugIn {} Installed.'.format(plugin_name))


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    install('RBE', '.')

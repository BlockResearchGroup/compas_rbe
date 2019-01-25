from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc
import traceback

from compas_rbe.rhino import AssemblyHelper


__commandname__ = "RBE_assembly_move_block"


def RunCommand(is_interactive):
    try:
        if 'RBE' not in sc.sticky:
            raise Exception('Initialise RBE first!')

        RBE = sc.sticky['RBE']

        assembly = RBE['assembly']

        keys = AssemblyHelper.select_vertices(assembly)
        if not keys:
            return

        if AssemblyHelper.update_vertex_attributes(assembly, keys):
            assembly.draw(RBE['settings'])

    except Exception as error:
        print(error)
        print(traceback.format_exc())


if __name__ == '__main__':

    RunCommand(True)

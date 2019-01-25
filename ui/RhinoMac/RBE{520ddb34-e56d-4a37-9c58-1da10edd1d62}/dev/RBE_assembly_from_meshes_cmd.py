from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


import scriptcontext as sc

import traceback

import compas_rhino
import compas_rbe

from compas_rbe.datastructures import Assembly


__commandname__ = "RBE_assembly_from_meshes"


def RunCommand(is_interactive):
    try:
        if 'RBE' not in sc.sticky:
            raise Exception('Initialise RBE first!')

        RBE = sc.sticky['RBE']

        guids = compas_rhino.select_meshes()

        RBE['assembly'] = assembly = Assembly()

        assembly.add_blocks_from_rhinomeshes(guids)
        assembly.draw(RBE['settings'])

    except Exception as error:
        print(error)
        print(traceback.format_exc())


if __name__ == '__main__':

    RunCommand(True)

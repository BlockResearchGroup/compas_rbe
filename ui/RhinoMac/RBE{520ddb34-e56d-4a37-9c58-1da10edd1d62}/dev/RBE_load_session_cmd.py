from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


import scriptcontext as sc

import os
import json
import traceback

import compas_rhino

from compas_rbe.datastructures import Assembly
from compas_rbe.datastructures import Block


HERE = os.path.abspath(os.path.dirname(__file__))
SESSIONS = os.path.join(HERE, '../sessions')


__commandname__ = "RBE_load_session"


def RunCommand(is_interactive):
    try:
        if 'RBE' not in sc.sticky:
            raise Exception('Initialise RBE first!')

        path = compas_rhino.select_file(folder=SESSIONS, filter='JSON files (*.json)|*.json||')
        if not path:
            return

        with open(path, 'r') as fo:
            data = json.load(fo)

        if 'RBE' in data:
            RBE = data['RBE']
        else:
            RBE = data

        if 'blocks' not in RBE:
            raise Exception('Session data is incomplete.')
        if 'assembly' not in RBE:
            raise Exception('Session data is incomplete.')
        if 'settings' not in RBE:
            raise Exception('Session data is incomplete.')

        blocks = {key: Block.from_data(data) for key, data in RBE['blocks'].items()}
        assembly = Assembly.from_data(RBE['assembly'])
        assembly.blocks = blocks

        sc.sticky['RBE']['settings'].update(RBE['settings'])
        sc.sticky['RBE']['assembly'] = assembly

        RBE = sc.sticky['RBE']

        assembly.draw(RBE['settings'])

    except Exception as error:
        print(error)
        print(traceback.format_exc())


if __name__ == '__main__':

    RunCommand(True)

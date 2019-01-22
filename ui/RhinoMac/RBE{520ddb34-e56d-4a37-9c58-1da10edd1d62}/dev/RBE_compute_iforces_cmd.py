from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc
import traceback

from compas.rpc import Proxy


proxy = Proxy('compas_rbe.equilibrium')
xcompute_iforces = proxy.compute_iforces_xfunc


def compute_iforces(assembly, solver):
    data = {
        'assembly': assembly.to_data(),
        'blocks': {str(key): assembly.blocks[key].to_data() for key in assembly.blocks},
    }
    result = xcompute_iforces(data, solver=solver)
    assembly.data = result['assembly']
    for key in assembly.blocks:
        assembly.blocks[key].data = result['blocks'][str(key)]


__commandname__ = "RBE_compute_iforces"


def RunCommand(is_interactive):
    try:
        if 'RBE' not in sc.sticky:
            raise Exception('Initialise RBE first!')

        RBE = sc.sticky['RBE']

        assembly = RBE['assembly']

        compute_iforces(assembly, RBE['settings']['solver'])

        assembly.draw(RBE['settings'])

    except Exception as error:
        print(error)
        print(traceback.format_exc())


if __name__ == '__main__':

    RunCommand(True)

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc
import traceback

from compas.rpc import Proxy


proxy = Proxy('compas_assembly.interfaces')
xidentify_interfaces = proxy.identify_interfaces_xfunc


def identify_interfaces(assembly, nmax=10, tmax=0.05, amin=0.01, lmin=0.01):
    data = {
        'assembly': assembly.to_data(),
        'blocks':
        {str(key): assembly.blocks[key].to_data()
         for key in assembly.blocks}
    }
    result = xidentify_interfaces(data, nmax=nmax, tmax=tmax, amin=amin, lmin=lmin)
    assembly.data = result['assembly']
    for key in assembly.blocks:
        assembly.blocks[key].data = result['blocks'][str(key)]


__commandname__ = "RBE_identify_interfaces"


def RunCommand(is_interactive):
    try:
        if 'RBE' not in sc.sticky:
            raise Exception('Initialise RBE first!')

        RBE = sc.sticky['RBE']
        assembly = RBE['assembly']

        identify_interfaces(assembly)

        assembly.draw(RBE['settings'])

    except Exception as error:
        print(error)
        print(traceback.format_exc())


if __name__ == '__main__':

    RunCommand(True)

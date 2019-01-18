from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc
import traceback

import compas_rhino
import compas_rbe

from compas_rhino.utilities import XFunc


xidentify_interfaces = XFunc('compas_rbe.interfaces.identify_interfaces_offset_xfunc', tmpdir=compas_rbe.TEMP)
xcompute_iforces = XFunc('compas_rbe.equilibrium.compute_iforces_xfunc', tmpdir=compas_rbe.TEMP)

xidentify_interfaces.paths = [compas_rbe.SRC]
xcompute_iforces.paths = [compas_rbe.SRC]


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


def compute_iforces(assembly, solver='CPLEX'):
    data = {
        'assembly': assembly.to_data(),
        'blocks':
        {str(key): assembly.blocks[key].to_data()
         for key in assembly.blocks},
    }
    result = xcompute_iforces(data, solver=solver)
    assembly.data = result['assembly']
    for key in assembly.blocks:
        assembly.blocks[key].data = result['blocks'][str(key)]


__commandname__ = "RBE_compute_interfaces_and_forces"


def RunCommand(is_interactive):
    try:
        if 'RBE' not in sc.sticky:
            raise Exception('Initialise RBE first!')

        RBE = sc.sticky['RBE']

        assembly = RBE['assembly']

        compas_rhino.clear_layer(RBE['settings']['layer'])
        sc.sticky['RBE'] = RBE

        xidentify_interfaces.python = RBE['settings']['pythonpath']
        xcompute_iforces.python = RBE['settings']['pythonpath']

        identify_interfaces(assembly)
        compute_iforces(assembly)

        assembly.draw(RBE['settings'])

    except Exception as error:
        print(error)
        print(traceback.format_exc())


if __name__ == '__main__':

    RunCommand(True)

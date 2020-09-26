from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# import warnings
# warnings.filterwarnings('ignore')
import json
import os
import compas

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import Block

# from .interfaceforces_cvx import *
from .interfaceforces_cvxopt import *


# def compute_interface_forces_xfunc(data, backend='CVXOPT', **kwargs):
#     assembly = Assembly.from_data(data['assembly'])
#     assembly.blocks = {int(key): Block.from_data(data['blocks'][key]) for key in data['blocks']}

#     # if backend == 'CVX':
#     #     compute_interface_forces_cvx(assembly, **kwargs)
#     if backend == 'CVXOPT':
#         compute_interface_forces_cvxopt(assembly, **kwargs)
#     else:
#         raise Exception('Backend not supported: {}'.format(backend))

#     return {
#         'assembly': assembly.to_data(),
#         'blocks': {str(key): assembly.blocks[key].to_data() for key in assembly.blocks},
#     }


__all__ = [name for name in dir() if not name.startswith('_')]

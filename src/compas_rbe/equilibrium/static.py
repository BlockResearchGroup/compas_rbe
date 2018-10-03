from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import sys

import compas

try:
    from numpy import array
    from numpy import zeros
    from numpy import ones
    from numpy import eye
    from numpy import identity
    from numpy import diagflat
    from numpy import absolute
except ImportError:
    if 'ironpython' not in sys.version.lower():
        raise

try:
    import cvxopt
    import cvxpy
except ImportError:
    if 'ironpython' not in sys.version.lower():
        raise

from .utilities import make_Aeq
from .utilities import make_Aiq


__author__    = ['Ursula Frick', 'Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = [
    'compute_interface_forces',
    'compute_interface_forces_xfunc'
]


def compute_interface_forces_xfunc(data, **kwargs):
    from compas_rbe.assemblies import Assembly
    from compas_rbe.assemblies import Block
    assembly = Assembly.from_data(data['assembly'])
    assembly.blocks = {int(key): Block.from_data(data['blocks'][key]) for key in data['blocks']}
    compute_interface_forces(assembly, **kwargs)
    return {
        'assembly': assembly.to_data(),
        'blocks': {str(key): assembly.blocks[key].to_data() for key in assembly.blocks}
    }


def compute_interface_forces(assembly,
                             friction8=False,
                             mu=0.6,
                             density=1.0,
                             verbose=False,
                             max_iters=100,
                             solver='ECOS'):
    r"""Compute the forces at the interfaces between the blocks of an assembly.

    Solve the following optimisation problem:

    .. math::


    Parameters
    ----------
    assembly : Assembly
        The rigid block assembly.
    friction8 : bool, optional
        Use an eight-sided friction pyramid.
        Default is False.

    """

    n = assembly.number_of_vertices()

    key_index = {key: index for index, key in enumerate(assembly.vertices())}

    fixed = [key for key in assembly.vertices_where({'is_support': True})]
    fixed = [key_index[key] for key in fixed]
    free  = [index for index in range(n) if index not in fixed]

    if verbose:
        print('')
        print(fixed)
        print(free)

    # ==========================================================================
    # equality constraints
    # ==========================================================================

    A, vcount = make_Aeq(assembly)
    A = A.toarray()
    A = A[[index * 6 + i for index in free for i in range(6)], :]

    b = [[0, 0, -1 * assembly.blocks[key].volume() * density, 0, 0, 0] for key in assembly.vertices()]
    b = array(b, dtype=float)
    b = b[free, :].reshape((-1, 1), order='C')
    # row-major ordering => fx, fy, fz, mx, my, mz, fx, fy, fz, mx, my, mz, ...

    # ==========================================================================
    # inequality constraints
    # ==========================================================================

    G = make_Aiq(vcount, False)
    G = G.toarray()

    h = zeros((G.shape[0], 1))

    # ==========================================================================
    # variables for the objective function
    # ==========================================================================

    a1 = 1.0   # weights on the compression forces
    a2 = 1e+5  # weights on the tension forces
    a3 = 1e+2  # weights on the friction forces (same as compression weights in Whiting)

    # add alpha := 1 / compression forces

    p = array([a1, a2, a3, a3] * vcount)
    P = diagflat(p)

    q = zeros((4 * vcount, 1))

    # ==========================================================================
    # weighting matrix
    # ==========================================================================

    # w = cvxpy.Variable(P.shape[0])

    # w = ones((P.shape[0], 1))
    # W = cvxpy.diag(w)

    # ==========================================================================
    # sanity check
    # ==========================================================================

    if verbose:
        print('')
        print('min   0.5 * xT * P * x + qT * x')
        print('s.t.  A * x == b')
        print('      G * x <= h')
        print('')
        print('with  P', P.shape)
        print('      q', q.shape)
        print('      G', G.shape)
        print('      h', h.shape)
        print('      A', A.shape)
        print('      b', b.shape)

    # instead do:
    # min   0.5 * xT * W * P * x (+ qT * x)

    # solve iteratively
    # at every iteration
    # update W based on the compression forces in the previous iteration
    # W is diagonal with
    # 1 / f+, 1, 1 / f+, 1 / f+

    # ==========================================================================
    # solve with cvxpy
    # ==========================================================================

    if compas.PY3:
        x = cvxpy.Variable((P.shape[0], 1))
    else:
        x = cvxpy.Variable(P.shape[0])

    objective = cvxpy.Minimize(0.5 * cvxpy.quad_form(x, P))

    constraints = [
        A * x == b,
        G * x <= h
    ]

    problem = cvxpy.Problem(objective, constraints)

    problem.solve(solver=cvxpy.ECOS, verbose=verbose, max_iters=max_iters)

    if problem.status == cvxpy.OPTIMAL:
        x = array(x.value).reshape((-1, 1))

        if verbose:
            print('')
            print('optimal value')
            print('-------------')
            print(problem.value)

    else:
        if x.value is not None:
            x = array(x.value).reshape((-1, 1))
        else:
            x = None

        if verbose:
            print('')
            print(problem.status)

    # ==========================================================================
    # solve with cvxopt
    # (use sparse matrices!)
    # ==========================================================================

    # res = cvxopt.solvers.qp(
    #     cvxopt.sparse(cvxopt.matrix(P), tc='d'),
    #     cvxopt.matrix(q),
    #     cvxopt.sparse(cvxopt.matrix(G), tc='d'),
    #     cvxopt.matrix(h),
    #     cvxopt.sparse(cvxopt.matrix(A), tc='d'),
    #     cvxopt.matrix(b)
    # )

    # x = array(res['x']).reshape((-1, 1))

    # if verbose:
    #     print res['primal objective']

    # ==========================================================================
    # update
    # ==========================================================================

    if x is not None:

        x[absolute(x) < 1e-6] = 0.0

        x = x.flatten().tolist()

        offset = 0

        for u, v, attr in assembly.edges(True):

            n = len(attr['interface_points'])

            attr['interface_forces'] = []

            for i in range(n):
                attr['interface_forces'].append({
                    'c_np': x[offset + 4 * i + 0],
                    'c_nn': x[offset + 4 * i + 1],
                    'c_u' : x[offset + 4 * i + 2],
                    'c_v' : x[offset + 4 * i + 3]
                })

            offset += 4 * n


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass

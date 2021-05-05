from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from numpy import array
from numpy import zeros
from numpy import diagflat
from numpy import absolute

import cvxopt

from compas_rbe.equilibrium.helpers import make_Aeq
from compas_rbe.equilibrium.helpers import make_Aiq


__all__ = [
    'compute_interface_forces_cvxopt',
]


def compute_interface_forces_cvxopt(assembly,
                                    friction8=False,
                                    mu=0.6,
                                    density=1.0,
                                    verbose=True,
                                    maxiters=1000):
    r"""Compute the forces at the interfaces between the blocks of an assembly.

    Parameters
    ----------
    assembly : Assembly
        The rigid block assembly.
    friction8 : bool, optional
        Use an eight-sided friction pyramid.
        Default is ``False``.
    mu : float, optional
        ?
    density : float, optional
        Density of the block material.
        Default is ``1.0``
    verbose : bool, optional
        Print information during the execution of the algorithm.
        Default is ``False``.
    maxiters : int, optional
        Maximum number of iterations used by the solver.
        Default is ``100``.

    Returns
    -------
    None
        The assembly is updated in place.

    Notes
    -----
    Solve the following optimisation problem:

    .. math::

        \begin{aligned}

            & \underset{x}{\text{minimise}} & \quad 0.5 \, \mathbf{x}^{T} \mathbf{P} \mathbf{x} + \mathbf{q}^{T} \mathbf{x} \\
            & \text{such that}              & \quad \mathbf{A} \mathbf{x} = \mathbf{b} \\
            &                               & \quad \mathbf{G} \mathbf{x} = \mathbf{h} \\

        \end{aligned}

    Examples
    --------
    .. code-block:: python

        pass

    References
    ----------
    The computational procedure for calculating the interface forces is described
    in detail in [Frick2015]_

    """

    n = assembly.number_of_nodes()

    node_index = {node: index for index, node in enumerate(assembly.nodes())}

    fixed = [node for node in assembly.nodes_where({'is_support': True})]
    fixed = [node_index[node] for node in fixed]
    free = list(set(range(n)) - set(fixed))

    # ==========================================================================
    # equality constraints
    # ==========================================================================

    A, vcount = make_Aeq(assembly)
    A = A.toarray()
    A = A[[index * 6 + i for index in free for i in range(6)], :]

    b = [[0, 0, -1 * assembly.node_attribute(node, 'block').volume() * density, 0, 0, 0] for node in assembly.nodes()]
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
    a3 = 1.0   # weights on the friction forces (same as compression weights in Whiting)

    p = array([a1, a2, a3, a3] * vcount)
    P = diagflat(p)

    q = zeros((4 * vcount, 1))

    # ==========================================================================
    # sanity check
    # ==========================================================================

    if verbose:
        print('')
        print('min   0.5 * xT * P * x (+ qT * x)')
        print('s.t.  A * x == b')
        print('      G * x <= h')
        print('')
        print('with  P', P.shape)
        print('      q', q.shape)
        print('      G', G.shape)
        print('      h', h.shape)
        print('      A', A.shape)
        print('      b', b.shape)

    # ==========================================================================
    # solve
    # ==========================================================================

    cvxopt.solvers.options['feastol'] = 1e-100
    cvxopt.solvers.options['maxiters'] = maxiters
    cvxopt.solvers.options['show_progress'] = verbose

    res = cvxopt.solvers.qp(
        cvxopt.sparse(cvxopt.matrix(P), tc='d'),
        cvxopt.matrix(q),
        cvxopt.sparse(cvxopt.matrix(G), tc='d'),
        cvxopt.matrix(h),
        cvxopt.sparse(cvxopt.matrix(A), tc='d'),
        cvxopt.matrix(b)
    )

    if res['status'] == 'optimal':
        x = array(res['x']).reshape((-1, 1))

        if verbose:
            print("Primal:", res['primal objective'])
            print("Dual:", res['primal objective'])

    else:
        if res['x']:
            x = array(res['x']).reshape((-1, 1))
        else:
            x = None

        if verbose:
            print('')
            print(res['status'])

    # ==========================================================================
    # update
    # ==========================================================================

    if x is not None:

        x[absolute(x) < 1e-6] = 0.0

        x = x.flatten().tolist()

        offset = 0

        for edge in assembly.edges():
            interface = assembly.edge_attribute(edge, 'interface')

            n = len(interface.points)

            interface.forces = []

            for i in range(n):
                interface.forces.append({
                    'c_np': x[offset + 4 * i + 0],
                    'c_nn': x[offset + 4 * i + 1],
                    'c_u': x[offset + 4 * i + 2],
                    'c_v': x[offset + 4 * i + 3]
                })

            offset += 4 * n

    return assembly


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass

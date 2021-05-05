from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas

from numpy import array
from numpy import zeros
from numpy import diagflat
from numpy import absolute
from numpy import float64

import cvxpy

from compas_rbe.equilibrium.helpers import make_Aeq
from compas_rbe.equilibrium.helpers import make_Aiq


__all__ = ['compute_interface_forces_cvx']


def compute_interface_forces_cvx(assembly,
                                 friction8=False,
                                 mu=0.6,
                                 density=1.0,
                                 verbose=False,
                                 maxiters=1000,
                                 solver=None):
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
    solver : {'OSQP', 'ECOS', 'CVXOPT', 'MOSEK', 'CPLEX'}, optional
        The solver to be used internally.
        Default is ``'ECOS'``.

    Returns
    -------
    None
        The assembly is updated in place.

    Notes
    -----
    This function solves the following optimisation problem:

    .. math::

        \begin{aligned}

            & \underset{x}{\text{minimise}} & \quad 0.5 \,
                                              \mathbf{x}^{T} \mathbf{P} \mathbf{x} + \mathbf{q}^{T} \mathbf{x} \\
            & \text{such that} & \quad \mathbf{A} \mathbf{x} = \mathbf{b} \\
            &                  & \quad \mathbf{G} \mathbf{x} <= \mathbf{h} \\

        \end{aligned}

    * CVXPY adaptive weights: https://www.cvxpy.org/examples/applications/sparse_solution.html
    * OOPQ-Eigen: https://github.com/ethz-asl/ooqp_eigen_interface
    * OOPQ: http://pages.cs.wisc.edu/~swright/ooqp/
    * HSL archive: http://www.hsl.rl.ac.uk/archive/index.html
    * CVXOPT qp: http://cvxopt.org/userguide/coneprog.html#quadratic-programming
    * CVXPY solver options: http://www.cvxpy.org/tutorial/advanced/index.html#setting-solver-options
    * Comparison of solver performance: https://scaron.info/blog/quadratic-programming-in-python.html
    * OSQP solver settings: https://osqp.org/docs/interfaces/solver_settings.html#solver-settings
    * CVXPY background: http://www.cvxpy.org/short_course/index.html

    Examples
    --------
    >>>

    References
    ----------
    The computational procedure for calculating the interface forces is described
    in detail in [Frick2015]_

    """
    if not solver:
        solver = 'ECOS'

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

    # b = [[0, 0, -1 * assembly.blocks[node].volume() * density, 0, 0, 0] for node in assembly.nodes()]

    b = [[0, 0, 0, 0, 0, 0] for i in range(n)]
    for node in assembly.nodes():
        block = assembly.node_attribute(node, 'block')
        index = node_index[node]
        b[index][2] = -1 * block.volume() * density

    b = array(b, dtype=float64)
    b = b[free, :].reshape((-1, 1), order='C')

    # print(A)
    # print(b)

    # print(A[:, :4])
    # print(A[:, 4:8])
    # print(A[:, 8:12])
    # print(A[:, 12:16])

    # row-major ordering => fx, fy, fz, mx, my, mz, fx, fy, fz, mx, my, mz, ...

    # ==========================================================================
    # inequality constraints
    # ==========================================================================

    G = make_Aiq(vcount, friction8, mu)
    G = G.toarray()

    # print(G.shape)

    h = zeros((G.shape[0], 1))

    # ==========================================================================
    # variables for the objective function
    # ==========================================================================

    a1 = 1.0   # weights on the compression forces
    a2 = 1e+5  # weights on the tension forces
    a3 = 1e+2  # weights on the friction forces (same as compression weights in Whiting)

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

    # solver_specific_opts

    if solver == 'ECOS':
        solver = cvxpy.ECOS
        # max_iters (100)
        # abstol (1e-7)
        # reltol (1e-6)
        # feastol (1e-7)
        # abstol_inacc (5e-5)
        # reltol_inacc (5e-5)
        # feastol_inacc (1e-4)

    elif solver == 'OSQP':
        solver = cvxpy.OSQP
        # max_iter (100)
        # ...

    elif solver == 'CVXOPT':
        solver = cvxpy.CVXOPT
        # max_iters (100)
        # abstol (1e-7)
        # reltol (1e-6)
        # feastol (1e-7)
        # refinement (1)
        # kktsolver ('chol', 'robust')

    elif solver == 'MOSEK':
        solver = cvxpy.MOSEK

    elif solver == 'CPLEX':
        solver = cvxpy.CPLEX

    else:
        raise Exception('Solver not supported: {}'.format(solver))

    if compas.PY3:
        x = cvxpy.Variable((P.shape[0], 1))
    else:
        x = cvxpy.Variable(P.shape[0])

    objective = cvxpy.Minimize(0.5 * cvxpy.quad_form(x, P))

    constraints = [
        A @ x == b,
        G @ x <= h
    ]

    problem = cvxpy.Problem(objective, constraints)

    problem.solve(solver=solver, verbose=verbose)

    # if not verbose:
    #     print(problem.status)

    # OPTIMAL
    # INFEASIBLE
    # UNBOUNDED
    # OPTIMAL_INACCURATE
    # INFEASIBLE_INACCURATE
    # UNBOUNDED_INACCURATE

    if problem.status == cvxpy.OPTIMAL:
        x = array(x.value).reshape((-1, 1))

    elif problem.status == cvxpy.OPTIMAL_INACCURATE:
        x = array(x.value).reshape((-1, 1))

    else:
        x = None

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

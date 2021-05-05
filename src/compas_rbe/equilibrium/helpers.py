from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import sqrt

from scipy.sparse import coo_matrix
from compas.geometry import cross_vectors


__all__ = [
    'make_Aeq',
    'make_Aiq',
]


def make_Aeq(assembly, return_vcount=True):
    """Create the equilibrium matrix.

    Parameters
    ----------
    assembly : compas_rbe.datastructures.Assembly
        The assembly for which the equality constraint matrix has to be constructed.
    return_vcount : bool, optional
        Include the total number of interface vertices in the return value.
        Default is `True`.

    Returns
    -------
    Aeq : coo_matrix
        A sparse representation of the coefficient matrix of the equality constraints.

    Examples
    --------
    >>>

    """
    rows = []
    cols = []
    data = []

    vcount = 0

    node_index = {node: index for index, node in enumerate(assembly.nodes())}

    for edge in assembly.edges():
        u, v = edge

        i = node_index[u]
        j = node_index[v]

        U = assembly.node_attribute(u, 'block')
        V = assembly.node_attribute(v, 'block')

        interface = assembly.edge_attribute(edge, 'interface')

        n = len(interface.points)

        # process the u block
        center = U.center()

        # B1
        block_rows, block_cols, block_data = _make_Aeq_block(interface, center, False)

        # shift rows and cols
        rows += [row + 6 * i for row in block_rows]
        cols += [col + 4 * vcount for col in block_cols]
        data += block_data

        # process the v block
        center = V.center()

        # B2
        block_rows, block_cols, block_data = _make_Aeq_block(interface, center, True)

        # shift rows and cols
        rows += [row + 6 * j for row in block_rows]
        cols += [col + 4 * vcount for col in block_cols]
        data += block_data

        # B1 and B2 have the same size
        # B1 and B2 occupy different rows in the same set of columns
        # B1 and B2 are both multiplied with the same interface forces

        vcount += n

    if return_vcount:
        return coo_matrix((data, (rows, cols))), vcount

    return coo_matrix((data, (rows, cols)))


def _make_Aeq_block(interface, center, reverse):
    """Create the sub matrix block of Aeq for interface k and block j."""

    rows = []
    cols = []
    data = []

    u = interface.frame.xaxis
    v = interface.frame.yaxis
    w = interface.frame.zaxis

    if reverse:
        u = [-1.0 * axis for axis in u]
        v = [-1.0 * axis for axis in v]
        w = [-1.0 * axis for axis in w]

    fx = [w[0], - w[0], u[0], v[0]]
    fy = [w[1], - w[1], u[1], v[1]]
    fz = [w[2], - w[2], u[2], v[2]]

    for i in range(len(interface.points)):

        xyz = interface.points[i]

        # coordinates of interface point
        # relative to block mass center
        rxyz = [center[axis] - xyz[axis] for axis in range(3)]

        # moments
        mu = cross_vectors(u, rxyz)
        mv = cross_vectors(v, rxyz)
        mw = cross_vectors(w, rxyz)

        mx = [mw[0], - mw[0], mu[0], mv[0]]
        my = [mw[1], - mw[1], mu[1], mv[1]]
        mz = [mw[2], - mw[2], mu[2], mv[2]]

        for j in range(4):
            col = j + (i * 4)
            # ?
            if fx[j]:
                rows.append(0)
                cols.append(col)
                data.append(fx[j])
            # ?
            if fy[j]:
                rows.append(1)
                cols.append(col)
                data.append(fy[j])
            # ?
            if fz[j]:
                rows.append(2)
                cols.append(col)
                data.append(fz[j])
            # ?
            if mx[j]:
                rows.append(3)
                cols.append(col)
                data.append(mx[j])
            # ?
            if my[j]:
                rows.append(4)
                cols.append(col)
                data.append(my[j])
            # ?
            if mz[j]:
                rows.append(5)
                cols.append(col)
                data.append(mz[j])

    return rows, cols, data


def make_Aiq(total_vcount, friction8=False, mu=0.6):
    r"""Construct the matrix of inequality constraints of a quadratic program.

    Parameters
    ----------
    total_vcount : int
        The total number of interface vertices.
    friction8 : bool, optional
        Use an 8-sided friction cone.
        Default is `False`.
    mu : float, optional
        The friction coefficient of the interface surfaces.

    Returns
    -------
    Aiq : coo_matrix
        A sparse representation of the coefficient matrix of the inequality constraints.

    Examples
    --------
    .. code-block:: python

        G = make_Aiq(vcount, False)
        G = G.toarray()

        objective = cvxpy.Minimize(0.5 * cvxpy.quad_form(x, P))

        constraints = [
            A * x == b,
            G * x <= h
        ]

        problem = cvxpy.Problem(objective, constraints)

    Notes
    -----
    In the optimisation problem

    .. math::

        \begin{aligned}
            & \underset{x}{\text{minimise}} & \quad 0.5 \, \mathbf{x}^{T} \mathbf{P} \mathbf{x} + \mathbf{q}^{T} \mathbf{x} \\
            & \text{such that} & \quad \mathbf{A} \mathbf{x}  = \mathbf{b} \\
            &                  & \quad \mathbf{G} \mathbf{x} \leq \mathbf{h} \\
        \end{aligned}

    :math:`\mathbf{x}` is the *4n-by-1* vector of 4 unknown contact force components
    per vertex of all *n* interface vertices

    .. math::

        \mathbf{x}[i:i+4] = [c^{n+}_{i}, c^{n-}_{i}, c^{u}_{i}, c^{v}_{i}]

    with

    * :math:`c^{n+}_{i}` the component in the direction of the interface frame normal (a "compression" contact)
    * :math:`c^{n-}_{i}` the component in the opposite direction of the interface frame normal (a "tension" contact)
    * :math:`c^{u}_{i}` the component in the direction of the interface frame *u* direction (a "friction" contact)
    * :math:`c^{v}_{i}` the component in the direction of the interface frame *v* direction (a "friction" contact)

    :math:`\mathbf{G}` is the *6n-by-4n* coefficient matrix of the 6 inequality constraints
    per vertex of all n interface vertices, as a function of the 4 unknown force components per vertex

    .. math::

        \mathbf{G}[i:i+6, j:j+4]
        =
        \begin{bmatrix}
             -1,  &  0, &  0, &  0 \\
              0,  & -1, &  0, &  0 \\
            -\mu, &  0, &  1, &  0 \\
            -\mu, &  0, & -1, &  0 \\
            -\mu, &  0, &  0, &  1 \\
            -\mu, &  0, &  0, & -1
        \end{bmatrix}

    Finally, :math:`\mathbf{h}` is a *6n-by-1* vector of zeros.

    Per verter per interface, this results in the following inequality constraints

    * :math:`-c^{n+}_{i} <= 0`
    * :math:`-c^{n-}_{i} <= 0`
    * :math:`-\mu c^{n+}_{i} + c^{u}_{i} <= 0`
    * :math:`-\mu c^{n+}_{i} - c^{u}_{i} <= 0`
    * :math:`-\mu c^{n+}_{i} + c^{v}_{i} <= 0`
    * :math:`-\mu c^{n+}_{i} - c^{v}_{i} <= 0`

    which basically express that, per interface vertex,
    the force components in both the positive and the negative direction of the
    interface normal have to be positive;
    and that the absolute values of both friction force components should be smaller
    than the friction force in the positive normal direction scaled by a factor :math:`\mu`.

    ..
        Note that the latter two constraints are enforced by requiring both the value
        and the opposite/negative value of the friction components to be smaller than
        :math:`\mu c^{n+}_{i}`, which is postive.

    References
    ----------

    """

    rows = []
    cols = []
    data = []
    c_8 = 1.0 / sqrt(2.0)

    # offsets

    i = 0
    j = 0

    for n in range(total_vcount):

        # negative (?) normal forces

        rows += [i, i + 1]
        cols += [j, j + 1]
        data += [-1, -1]

        # friction4

        rows += [i + 2, i + 2, i + 3, i + 3, i + 4, i + 4, i + 5, i + 5]
        cols += [j, j + 2, j, j + 2, j, j + 3, j, j + 3]
        data += [-mu, 1, -mu, -1, -mu, 1, -mu,    -1]

        if not friction8:
            i += 6
        else:
            rows += [i + 6, i + 6, i + 6]
            cols += [j, j + 2, j + 3]
            data += [-mu, c_8, c_8]

            rows += [i + 7, i + 7, i + 7]
            cols += [j, j + 2, j + 3]
            data += [-mu, -c_8, -c_8]

            rows += [i + 8, i + 8, i + 8]
            cols += [j, j + 2, j + 3]
            data += [-mu, c_8, -c_8]

            rows += [i + 9, i + 9, i + 9]
            cols += [j, j + 2, j + 3]
            data += [-mu, -c_8, c_8]

            i += 10

        j += 4

    return coo_matrix((data, (rows, cols)))


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass

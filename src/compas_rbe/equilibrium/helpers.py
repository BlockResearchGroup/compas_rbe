from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import sys
from math import sqrt

import compas

try:
    from scipy.sparse import coo_matrix
except ImportError:
    compas.raise_if_not_ironpython()

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

    """
    rows = []
    cols = []
    data = []

    vcount = 0

    key_index = {key: index for index, key in enumerate(assembly.vertices())}

    for u, v, attr in assembly.edges(True):

        i = key_index[u]
        j = key_index[v]

        interface = {
            'points' : attr['interface_points'],
            'uvw'    : attr['interface_uvw'],
        }

        n = len(interface['points'])

        # process the u block
        center = assembly.blocks[u].center()

        block_rows, block_cols, block_data = _make_Aeq_block(interface, center, False)

        # shift rows and cols
        rows += [row + 6 * i for row in block_rows]
        cols += [col + 4 * vcount for col in block_cols]
        data += block_data

        # process the v block
        center = assembly.blocks[v].center()

        block_rows, block_cols, block_data = _make_Aeq_block(interface, center, True)

        # shift rows and cols
        rows += [row + 6 * j for row in block_rows]
        cols += [col + 4 * vcount for col in block_cols]
        data += block_data

        vcount += n

    if return_vcount:
        return coo_matrix((data, (rows, cols))), vcount

    return coo_matrix((data, (rows, cols)))


def _make_Aeq_block(interface, center, reverse):
    """Create the sub matrix block of Aeq for interface k and block j."""

    rows = []
    cols = []
    data = []

    u, v, w = interface['uvw']

    if reverse:
        u = [-1.0 * axis for axis in u]
        v = [-1.0 * axis for axis in v]
        w = [-1.0 * axis for axis in w]

    fx = [w[0], - w[0], u[0], v[0]]
    fy = [w[1], - w[1], u[1], v[1]]
    fz = [w[2], - w[2], u[2], v[2]]

    for i in range(len(interface['points'])):

        xyz = interface['points'][i]

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
    """Construct the matrix of inequality constraints."""

    rows = []
    cols = []
    data = []
    c_8  = 1.0 / sqrt(2.0)

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
        data += [-mu, 1, -mu, -1, -mu, 1, -mu, -1]

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

********************************************************************************
Introduction
********************************************************************************

.. figure:: /_images/compas_rbe.jpg
    :figclass: figure
    :class: figure-img img-fluid


Rigid Block Equilibrium Analysis
================================

:mod:`compas_rbe` provides functionality for computing the set of contact forces
at the interfaces between the rigid blocks of a *discrete element assembly*
that establish equilibrium with the smallest amount of tension forces possible,
i.e. it favours solutions with only compression forces and friction.

.. note::

    For more information on discrete element assemblies, see the docs of :mod:`compas_assembly`.


It solves the following quadratic optimisation problem,
with linear equality and inequality constraints

.. math::

    \begin{aligned}
        & \underset{x}{\text{minimise}} & \quad 0.5 \, \mathbf{x}^{T} \mathbf{P} \mathbf{x} + \mathbf{q}^{T} \mathbf{x} \\
        & \text{such that} & \quad \mathbf{A} \mathbf{x}  = \mathbf{b} \\
        &                  & \quad \mathbf{G} \mathbf{x} \leq \mathbf{h} \\
    \end{aligned}

:math:`\mathbf{x}` is the *4n-by-1* vector of the 4 unknown contact force component
magnitudes per vertex of all *n* interface vertices of the assembly, along the directions
of the frame axes of the respective interfaces.
For vertex *i* belonging to interface *k* we have

.. math::

    \mathbf{x}[i:i+4] =
    \begin{bmatrix}
        c^{n+}_{i} \\
        c^{n-}_{i} \\
        c^{u}_{i} \\
        c^{v}_{i}
    \end{bmatrix}

with

* :math:`c^{n+}_{i}` the component in the direction of the frame normal of interface *k* (a "compression" contact)
* :math:`c^{n-}_{i}` the component in the opposite direction of the frame normal of interface *k* (a "tension" contact)
* :math:`c^{u}_{i}` the component in the direction of the frame *u* direction of interface *k* (a "friction" contact)
* :math:`c^{v}_{i}` the component in the direction of the frame *v* direction of interface *k* (a "friction" contact)

.. note::

    The vertices are grouped per interface.
    For example, if interface *k* has 4 vertices, then the force magnitudes along the
    frame directions per vertex of the interface are

    .. math::

        \begin{aligned}
            & \mathbf{v}_{i + 0} & = \mathbf{v}_{k, 0} & = \mathbf{x}[i:i+4]    \\
            & \mathbf{v}_{i + 1} & = \mathbf{v}_{k, 1} & = \mathbf{x}[i+4:i+8]  \\
            & \mathbf{v}_{i + 2} & = \mathbf{v}_{k, 2} & = \mathbf{x}[i+8:i+12] \\
            & \mathbf{v}_{i + 3} & = \mathbf{v}_{k, 3} & = \mathbf{x}[i+12:i+16]
        \end{aligned}


Quadratic energy
----------------


Equality constraints
--------------------


Inequality constraints
----------------------

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

:math:`\mathbf{h}` is a *6n-by-1* vector of zeros.

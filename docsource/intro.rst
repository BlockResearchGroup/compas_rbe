********************************************************************************
Rigid Block Equilibrium Analysis
********************************************************************************

.. figure:: /_images/compas_rbe.jpg
    :figclass: figure
    :class: figure-img img-fluid

    Rigid-block model of ...


Introduction
============

:mod:`compas_rbe` provides functionality for computing the set of contact forces
at the interfaces between the rigid blocks of a *discrete element assembly*
that establish equilibrium with the smallest amount of tension forces possible,
i.e. it favours solutions with only compression forces and friction.


Assembly data structure
=======================

Assemblies of rigid blocks are represented with an ``Assembly`` data structure.
A basic ``Assembly`` data structure is defined in :mod:`compas_assembly` and extended
here for the specific needs of the equilibrium analysis calculations.

An ``Assembly`` data structure is essentially a network of vertices connected by edges.
Each node corresponds to one rigid block in the assembly.
Each edge corresponds to an interface between two blocks.

The blocks are represented by ``Block`` data structures. A ``Block`` is essentially
a closed ``Mesh`` with some additional functionality. The base ``Block`` is also
defined in :mod:`compas_assembly` and extended here.

For more information about ``Assembly`` and ``Block``, see ...


Quadratic Program
=================

:mod:`compas_rbe` finds a feasible equilibrium state by solving the following
quadratic optimisation problem with linear equality and inequality constraints

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
            & \mathbf{v}_{i + 0} & = \mathbf{v}_{k, 0} \quad & = \mathbf{x}[i:i+4] \\
            & \mathbf{v}_{i + 1} & = \mathbf{v}_{k, 1} \quad & = \mathbf{x}[i+4:i+8] \\
            & \mathbf{v}_{i + 2} & = \mathbf{v}_{k, 2} \quad & = \mathbf{x}[i+8:i+12] \\
            & \mathbf{v}_{i + 3} & = \mathbf{v}_{k, 3} \quad & = \mathbf{x}[i+12:i+16]
        \end{aligned}


Energy
------

The quadratic energy of the optimisation problem is formulated as

.. math::

    0.5 \, \mathbf{x}^{T} \mathbf{P} \mathbf{x} + \mathbf{q}^{T} \mathbf{x}


This is essentially the sum of all squared, unknown contact force components at the
vertices of the interfaces, with each type of force component weighted by a penalty factor.

:math:`\mathbf{P}` is the *4n-by-4n* weighting matrix with the following factors
repeated along its diagonal

.. math ::

    \begin{aligned}
        & c^{n+} & \Rightarrow \quad & 1.0 \\
        & c^{n-} & \Rightarrow \quad & 1e^{+5} \\
        & c^{u}  & \Rightarrow \quad & 1.0 \\
        & c^{v}  & \Rightarrow \quad & 1.0
    \end{aligned}

The forces along the negative normal directions of the interface frames are
thus heavily penalised. The goal is to find an equilibrium state that requires
as little adhesion between the blocks as possible, and relies only on compression
and friction.


Equality constraints
--------------------

.. seealso::

    :func:`compas_rbe.equilibrium.make_Aeq`

The equality constraints represent the necessary conditions for the assembly to be
in static equilibrium. They express the equilibrium of forces at the vertices of
the interfaces between the blocks.

:math:`\mathbf{A}` is the *6n-by-4n* coefficient matrix of the 6 equilibrium equations
per vertex of the *n* interface vertices, as a function of the 4 unknown force
components per vertex.

.. math::

    \mathbf{A}[i:i+6, j:j+4]
    =
    \begin{bmatrix}
         -1,  &  0, &  0, &  0 \\
          0,  & -1, &  0, &  0 \\
        -\mu, &  0, &  1, &  0 \\
        -\mu, &  0, & -1, &  0 \\
        -\mu, &  0, &  0, &  1 \\
        -\mu, &  0, &  0, & -1
    \end{bmatrix}

.. note::

    Vertex *i* of the interface vertices belongs to a particular interface *k*
    which is the contact surface between exactly two blocks *m* and *n*.


Inequality constraints
----------------------

.. seealso::

    :func:`compas_rbe.equilibrium.make_Aiq`


:math:`\mathbf{G}` is the *6n-by-4n* coefficient matrix of the 6 inequality constraints
per vertex of the *n* interface vertices, as a function of the 4 unknown force
components per vertex.

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

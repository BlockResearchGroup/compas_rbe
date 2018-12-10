"""
********************************************************************************
compas_rbe.datastructures
********************************************************************************

.. figure:: /_images/compas_rbe-assembly_interfaces.png
    :figclass: figure
    :class: figure-img img-fluid


.. currentmodule:: compas_rbe.datastructures


Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Assembly
    Block

"""

from __future__ import absolute_import, division, print_function

from .assembly import *
from .block import *

__all__ = [name for name in dir() if not name.startswith('_')]

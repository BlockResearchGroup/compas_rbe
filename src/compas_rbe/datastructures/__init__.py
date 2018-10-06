"""
********************************************************************************
compas_rbe.datastructures
********************************************************************************

.. figure:: /_images/compas_rbe-assembly_interfaces.png
    :figclass: figure
    :class: figure-img img-fluid


.. currentmodule:: compas_rbe.datastructures


.. autosummary::
    :toctree: generated/
    :nosignatures:

    Assembly
    Block

"""

from __future__ import absolute_import

from . import assembly
from . import block
from . import interface

from .assembly import *
from .block import *
from .interface import *

__all__ = assembly.__all__ + block.__all__ + interface.__all__

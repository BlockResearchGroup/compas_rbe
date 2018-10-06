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


Functions
=========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    identify_interfaces


"""

from __future__ import absolute_import

from .assembly import *
from .block import *
from .interface import *

from . import assembly
from . import block
from . import interface

__all__ = assembly.__all__ + block.__all__ + interface.__all__

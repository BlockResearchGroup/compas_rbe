from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_assembly.datastructures import Assembly


__all__ = ['Assembly']


# should an assembly be composed of a network attribute
# and a block collection
# rather than inherit from network
# and add inconsistent stuff to that interface?


class Assembly(Assembly):

    __module__ = 'compas_rbe.datastructures'


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass

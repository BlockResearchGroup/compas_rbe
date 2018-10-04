from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.viewers.core import App

from compas_rbe.viewer.view import View
from compas_rbe.viewer.controller import Controller

from compas_rbe.viewer import CONFIG
from compas_rbe.viewer import STYLE


__all__ = ['AssemblyViewer']


class AssemblyViewer(App):
    """"""

    def __init__(self):
        super(AssemblyViewer, self).__init__(CONFIG, STYLE)
        self.controller = Controller(self)
        self.view = View(self.controller)
        self.setup()
        self.init()
        self.view.glInit()
        self.view.setup_grid()

    @property
    def assembly(self):
        return self.controller.assembly

    @assembly.setter
    def assembly(self, assembly):
        self.controller.assembly = assembly
        self.controller.center_assembly()
        self.view.glInit()
        self.view.make_buffers()
        self.view.updateGL()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    pass

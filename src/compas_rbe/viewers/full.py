from __future__ import print_function

import json

from PySide.QtCore import Qt

from PySide.QtGui import QBoxLayout
from PySide.QtGui import QGridLayout
from PySide.QtGui import QWidget
from PySide.QtGui import QCheckBox
from PySide.QtGui import QLabel
from PySide.QtGui import QFileDialog

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from compas_rbe.viewers.basic import AssemblyViewerBasic

from compas_rbe.rbe.block import Block
from compas_rbe.rbe.assembly import Assembly

from compas_rbe.rbe.interfaces import identify_interfaces
from compas_rbe.rbe.equilibrium import compute_interface_forces


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = ['AssemblyViewerFull', ]


class AssemblyViewerFull(AssemblyViewerBasic):
    """"""

    def __init__(self):
        super(AssemblyViewerFull, self).__init__()

    def setup(self):
        super(AssemblyViewerFull, self).setup()
        self.setup_menubar()
        self.setup_statusbar()

    def setup_menubar(self):
        self.menu = menu = self.main.menuBar()
        self.main.setMenuBar(menu)
        self.add_file_menu()
        self.add_rbe_menu()

    def add_file_menu(self):
        menu = self.menu.addMenu('&File')
        open_action = menu.addAction('&Open...')
        open_action.triggered.connect(self.do_open)

    def do_open(self):
        res = QFileDialog.getOpenFileName(
            caption="Select a JSON file to open.",
            dir="",
            filter="*.json"
        )
        if res:
            filename, selected_filter = res
            self.view.assembly = self.assembly = Assembly()

            with open(filename, 'rb') as fp:
                data = json.load(fp)
                for item in data:
                    block = Block.from_data(item)
                    self.assembly.add_block(block)

            for key, attr in self.assembly.vertices_iter(True):
                if self.assembly.blocks[key].attributes['name'] == 'Block_0':
                    attr['is_support'] = True
        self.view.updateGL()

    def add_rbe_menu(self):
        menu = self.menu.addMenu('&RBE')
        # identify interfaces
        identify_action = menu.addAction('&Identify interfaces')
        identify_action.triggered.connect(self.do_identify)
        # compute contact forces
        compute_action = menu.addAction('&Compute contact forces')
        compute_action.triggered.connect(self.do_compute)

    def do_identify(self):
        identify_interfaces(
            self.assembly,
            nmax=5,
            tmax=0.05,
            amin=0.01,
            lmin=0.01,
        )
        self.view.updateGL()

    def do_compute(self):
        compute_interface_forces(self.assembly)
        self.view.updateGL()

    def setup_statusbar(self):
        self.status = self.main.statusBar()
        self.main.setStatusBar(self.status)
        self.status.showMessage('test')


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    pass

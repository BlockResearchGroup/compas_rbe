from __future__ import print_function

import sys

from PySide.QtCore import Qt

from PySide.QtGui import QMainWindow
from PySide.QtGui import QApplication
from PySide.QtGui import QDockWidget
from PySide.QtGui import QBoxLayout
from PySide.QtGui import QGridLayout
from PySide.QtGui import QWidget
from PySide.QtGui import QCheckBox
from PySide.QtGui import QLabel

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from compas_rbe.viewers.view import View


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = ['AssemblyViewerBasic', ]


class AssemblyViewerBasic(QApplication):
    """"""

    def __init__(self, assembly=None):
        super(AssemblyViewerBasic, self).__init__(sys.argv)
        self.assembly = assembly
        self.setup()

    def setup(self):
        self.main = QMainWindow()
        self.main.setFixedSize(1264, 768)
        self.setup_view()
        self.setup_sidebar()

    def start(self):
        self.main.show()
        sys.exit(self.exec_())

    def setup_view(self):
        self.view = view = View(self.assembly)
        view.setFocusPolicy(Qt.StrongFocus)
        view.setFocus()
        self.main.setCentralWidget(view)

    def setup_sidebar(self):
        self.sidebar = sidebar = QDockWidget()
        sidebar.setAllowedAreas(Qt.LeftDockWidgetArea)
        sidebar.setFeatures(QDockWidget.NoDockWidgetFeatures)
        sidebar.setFixedWidth(240)
        widget = QWidget(sidebar)
        layout = QBoxLayout(QBoxLayout.TopToBottom)
        toggles = QGridLayout()
        # toggles
        title = QLabel('Assembly Visibility')
        title.setStyleSheet("QLabel { background-color: white; color: black; padding: 5px; }")
        toggles.addWidget(title, 0, 0)
        # toggle vertices
        toggle = QCheckBox('vertices')
        toggle.setCheckState(self.view.vertices_on)
        toggles.addWidget(toggle, 1, 0)

        def change(state):
            self.view.vertices_on = state
            self.view.updateGL()

        toggle.stateChanged.connect(change)
        # toggle edges
        toggle = QCheckBox('edges')
        toggle.setCheckState(self.view.edges_on)
        toggles.addWidget(toggle, 2, 0)

        def change(state):
            self.view.edges_on = state
            self.view.updateGL()

        toggle.stateChanged.connect(change)
        # toggle faces
        toggle = QCheckBox('faces')
        toggle.setCheckState(self.view.faces_on)
        toggles.addWidget(toggle, 3, 0)

        def change(state):
            self.view.faces_on = state
            self.view.updateGL()

        toggle.stateChanged.connect(change)
        # toggle interfaces
        toggle = QCheckBox('interfaces')
        toggle.setCheckState(self.view.interfaces_on)
        toggles.addWidget(toggle, 4, 0)

        def change(state):
            self.view.interfaces_on = state
            self.view.updateGL()

        toggle.stateChanged.connect(change)
        # toggle forces
        toggle = QCheckBox('forces')
        toggle.setCheckState(self.view.forces_on)
        toggles.addWidget(toggle, 5, 0)

        def change(state):
            self.view.forces_on = state
            self.view.updateGL()

        toggle.stateChanged.connect(change)
        # combine
        layout.addLayout(toggles)
        layout.addStretch()
        widget.setLayout(layout)
        sidebar.setWidget(widget)
        self.main.addDockWidget(Qt.LeftDockWidgetArea, sidebar)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    pass

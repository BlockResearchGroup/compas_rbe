from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


import os
import sys

import rhinoscriptsyntax as rs
import scriptcontext as sc

import Rhino
import Rhino.UI

import clr
clr.AddReference("Eto")
clr.AddReference("Rhino.UI")

import Eto
import Eto.Drawing as drawing
import Eto.Forms as forms

import compas_rhino
import compas_rbe


__commandname__ = "RBE_settings"


class UpdateSettingsForm(forms.Dialog[bool]):
    
    def __init__(self, settings):
        self._settings = None
        self.settings = settings

        self.Title = 'RBE: update settings'
        self.Padding = drawing.Padding(12)
        self.Resizable = True

        self.init()

    def init(self):
        self.table = table = forms.GridView()
        table.ShowHeader = True
        table.DataStore = [[name, value] for name, value in zip(self.names, self.values)]

        c1 = forms.GridColumn()
        c1.HeaderText = 'Name'
        c1.Editable = False
        c1.DataCell = forms.TextBoxCell(0)
        table.Columns.Add(c1)

        c2 = forms.GridColumn()
        c2.HeaderText = 'Value'
        c2.Editable = True
        c2.DataCell = forms.TextBoxCell(1)
        table.Columns.Add(c2)

        layout = forms.DynamicLayout()
        layout.Spacing = drawing.Size(12, 12)
        layout.BeginVertical()
        layout.AddRow(table)
        layout.EndVertical()
        layout.AddSeparateRow(None, self.ok, self.cancel, None)

        self.Content = layout

    @property
    def ok(self):
        self.DefaultButton = forms.Button(Text='OK')
        self.DefaultButton.Click += self.on_ok
        return self.DefaultButton

    @property
    def cancel(self):
        self.AbortButton = forms.Button(Text='Cancel')
        self.AbortButton.Click += self.on_cancel
        return self.AbortButton

    @property
    def settings(self):
        return self._settings

    @settings.setter
    def settings(self, settings):
        self._settings = settings.copy()
        self._names = names = sorted(settings.keys())
        self._values = [settings[name] for name in names]

    @property
    def names(self):
        return self._names

    @property
    def values(self):
        return self._values
    
    def on_ok(self, sender, e):
        try:
            for i, name in enumerate(self.names):
                self._settings[name] = self.table.DataStore[i][1]
        except Exception as e:
            print(e)
            self.Close(False)
        self.Close(True)

    def on_cancel(self, sender, e):
        self.Close(False)


# ==============================================================================
# The Command
# ==============================================================================


def RunCommand(is_interactive):
    if not 'RBE' in sc.sticky:
        raise Exception('Initialise RBE first!')

    RBE = sc.sticky['RBE']

    try:

        dialog = UpdateSettingsForm(RBE['settings'])
        
        if dialog.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow):
            RBE['settings'].update(dialog.settings)

        print(RBE['settings'])

    except Exception as error:

        print(error)

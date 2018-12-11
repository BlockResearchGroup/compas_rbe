from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
import sys
from ast import literal_eval

import compas

try:
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

    Dialog = forms.Dialog[bool]

except ImportError:
    compas.raise_if_ironpython()

    class Dialog: pass

import compas_rhino
import compas_rbe


__all__ = ['UpdateSettingsForm']


class UpdateSettingsForm(Dialog):

    def __init__(self, settings):
        self._settings = None
        self._names = None
        self._values = None
        self.settings = settings

        self.table = table = forms.GridView()
        table.ShowHeader = True
        table.DataStore = [[name, value] for name, value in zip(self.names, self.values)]
        table.Height = 300

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

        layout.AddRow(table)
        layout.Add(None)
        layout.BeginVertical()
        layout.BeginHorizontal()
        layout.AddRow(None, self.ok, self.cancel)
        layout.EndHorizontal()
        layout.EndVertical()

        self.Title = 'RBE: update settings'
        self.Padding = drawing.Padding(12)
        self.Resizable = False
        self.Content = layout
        self.ClientSize = drawing.Size(400, 600)

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
        self._values = [repr(settings[name]) for name in names]

    @property
    def names(self):
        return self._names

    @property
    def values(self):
        return self._values

    def on_ok(self, sender, e):
        try:
            for i, name in enumerate(self.names):
                data = self.table.DataStore[i][1]
                try:
                    value = literal_eval(data)
                except Exception:
                    value = data
                self._settings[name] = value
        except Exception as e:
            print(e)
            self.Close(False)
        self.Close(True)

    def on_cancel(self, sender, e):
        self.Close(False)


# dialog = SampleEtoDialog()
# dialog.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)

# result = rs.CheckListBox([('a', True), ('b', False)], "Toggle states", "CheckListBox")
# result = rs.RealBox("Enter a number", 10, "", 0, 1000)
# result = rs.StringBox()
# print(result)

# for name in dir(forms):
#     print(name)

# AboutDialog
# ColorDialog
# CommonDialog
# FileDialog
# FontDialog
# OpenFileDialog
# OpenWithDialog
# PrintDialog
# SaveFileDialog
# SelectFolderDialog

# dialog = forms.AboutDialog()
# dialog = forms.ColorDialog()  # causes Rhino to crash
# dialog = forms.FileDialog()

# dialog.ShowDialog()

# AboutDialog
# AddValueEventArgs
# Application
# AutoSelectMode
# BindableBinding
# BindableExtensions
# BindableWidget
# Binding
# BindingChangedEventArgs
# BindingChangingEventArgs
# BindingCollection
# BindingExtensions
# BindingUpdateMode
# BorderType
# Button
# ButtonImagePosition
# ButtonMenuItem
# ButtonToolItem
# Calendar
# CalendarMode
# Cell
# CellEventArgs
# CellPaintEventArgs
# CellStates
# CheckBox
# CheckBoxCell
# CheckCommand
# CheckMenuItem
# CheckToolItem
# Clipboard
# ColorDialog
# ColorPicker
# ColumnBinding
# ComboBox
# ComboBoxCell
# Command
# CommonControl
# CommonDialog
# Container
# ContextMenu
# Control
# ControlBinding
# Cursor
# CursorType
# Cursors
# CustomCell
# DataStoreCollection
# DataStoreVirtualCollection
# DateTimePicker
# DateTimePickerMode
# DelegateBinding
# Dialog
# DialogDisplayMode
# DialogResult
# DirectBinding
# DockPosition
# DocumentControl
# DocumentPage
# DocumentPageEventArgs
# Drawable
# DrawableCell
# DrawableCellPaintEventArgs
# DrawableCellStates
# DropDown
# DualBinding
# DualBindingMode
# DynamicControl
# DynamicItem
# DynamicLayout
# DynamicRow
# DynamicTable
# EnumDropDown
# EnumRadioButtonList
# Expander
# FileDialog
# FileDialogFilter
# FileFilter
# FilePicker
# FilterCollection
# FixedMaskedTextProvider
# FontDialog
# FontPicker
# Form
# Grid
# GridCell
# GridCellFormatEventArgs
# GridColumn
# GridColumnCollection
# GridColumnEventArgs
# GridItem
# GridLines
# GridView
# GridViewCellEventArgs
# GroupBox
# HorizontalAlign
# HorizontalAlignment
# IBindable
# IBinding
# IColumnItem
# ICommandItem
# IContextMenuHost
# IDataStore
# IImageListItem
# IIndirectBinding
# IKeyboardInputSource
# IListItem
# IMaskedTextProvider
# IMouseInputSource
# INavigationItem
# ISelectable
# ISelectableControl
# ISelectionPreserver
# ISubmenu
# ITextBuffer
# ITreeGridItem
# ITreeGridStore
# ITreeItem
# ITreeStore
# IValueConverter
# ImageListItem
# ImageTextCell
# ImageView
# ImageViewCell
# IndirectBinding
# InsertKeyMode
# KeyEventArgs
# KeyEventType
# Keyboard
# Keys
# KeysExtensions
# Label
# Layout
# LinkButton
# ListBox
# ListControl
# ListItem
# ListItemCollection
# MaskedTextBox
# MaskedTextStepper
# Menu
# MenuBar
# MenuBarSystemItems
# MenuItem
# MenuItemCollection
# MessageBox
# MessageBoxButtons
# MessageBoxDefaultButton
# MessageBoxType
# Mouse
# MouseButtons
# MouseEventArgs
# Navigation
# NavigationItem
# NavigationItemEventArgs
# Notification
# NumericMaskedTextBox
# NumericMaskedTextProvider
# NumericMaskedTextStepper
# NumericStepper
# NumericUpDown
# ObjectBinding
# OpenFileDialog
# OpenWithDialog
# Orientation
# PageOrientation
# PageSettings
# PaintEventArgs
# Panel
# PasswordBox
# PixelLayout
# PrintDialog
# PrintDocument
# PrintPageEventArgs
# PrintSelection
# PrintSettings
# ProgressBar
# ProgressCell
# PropertyBinding
# PropertyCell
# PropertyCellType
# PropertyCellTypeBoolean
# PropertyCellTypeColor
# PropertyCellTypeDateTime
# PropertyCellTypeDropDown
# PropertyCellTypeEnum
# PropertyCellTypeString
# RadioButton
# RadioButtonList
# RadioButtonListOrientation
# RadioCommand
# RadioMenuItem
# RadioToolItem
# Range
# RangeExtensions
# RelayCommand
# RichTextArea
# RichTextAreaFormat
# SaveFileDialog
# Screen
# ScrollEventArgs
# Scrollable
# SearchBox
# SelectFolderDialog
# SelectableFilterCollection
# SeparatorMenuItem
# SeparatorToolItem
# SeparatorToolItemType
# SingleValueCell
# Slider
# SliderOrientation
# Spinner
# Splitter
# SplitterFixedPanel
# SplitterOrientation
# StackLayout
# StackLayoutItem
# Stepper
# StepperDirection
# StepperEventArgs
# StepperValidDirections
# SubmenuExtensions
# TabControl
# TabPage
# TableCell
# TableLayout
# TableRow
# TextAlignment
# TextArea
# TextBox
# TextBoxCell
# TextBufferExtensions
# TextChangingEventArgs
# TextControl
# TextInputEventArgs
# TextReplacements
# TextStepper
# ThemedContainerHandler
# ThemedControlHandler
# ThemedControls
# Tool
# ToolBar
# ToolBarDock
# ToolBarTextAlign
# ToolItem
# ToolItemCollection
# TrayIndicator
# TreeGridCell
# TreeGridItem
# TreeGridItemCollection
# TreeGridView
# TreeGridViewItemCancelEventArgs
# TreeGridViewItemEventArgs
# TreeItem
# TreeItemCollection
# TreeView
# TreeViewItemCancelEventArgs
# TreeViewItemEditEventArgs
# TreeViewItemEventArgs
# UITimer
# VariableMaskedTextProvider
# VerticalAlign
# VerticalAlignment
# WebView
# WebViewLoadedEventArgs
# WebViewLoadingEventArgs
# WebViewNewWindowEventArgs
# WebViewTitleEventArgs
# WidgetExtensions
# Window
# WindowState
# WindowStyle
# WrapMode

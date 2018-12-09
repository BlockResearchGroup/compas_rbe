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


__all__ = []


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

"""Subclass of panel_control_parameters, which is generated by wxFormBuilder."""

import wx
import GUI_control_parameters
import Panel_edit_paras_overwrite
from test.data.control_parameters import parameters_object
from test.control import control_parameters
from test.control.tools import view_tools
# Implementing panel_control_parameters
class panel_control_paras( GUI_control_parameters.panel_control_parameters ):
	def __init__( self, parent, id, pos, size, style ):
		GUI_control_parameters.panel_control_parameters.__init__( self, parent )
		self.control = control_parameters.Control(self)
		view_tools.config_control(self, id, pos, size, style)

	# Handlers for panel_control_parameters events.
	def refresh_paras_panel( self, event ):
		# TODO: Implement refresh_paras_panel
		show_content = self.control.load_show_content()
		sizer = self.GetSizer()
		sizer.Clear()
		for key, values in (show_content.iterkeys(), show_content.itervalues()):

			panel = Panel_edit_paras_overwrite.panel_edit_paras(self)
			panel.m_staticText_paraname.SetLabel(key)
			panel.m_textCtrl_paravalue.SetValue(values)
			sizer.Add( panel, 0, 0, 5 )
		print 'layout'
		sizer.Layout()
	
	

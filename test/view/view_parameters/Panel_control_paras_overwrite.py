"""Subclass of panel_control_parameters, which is generated by wxFormBuilder."""

import wx
import GUI_control_parameters
from LuaProgrammingGUI.test.control.control_parameters import control_parameters
from LuaProgrammingGUI.test.control.control_process import control_process_showdata
from LuaProgrammingGUI.test.control.tools import view_tools
from LuaProgrammingGUI.test.control.tools import controlfile_tools
try:
    from wx.lib.pubsub import pub
except ImportError:
    from pubsub import pub

# Implementing panel_control_parameters
class panel_control_paras( GUI_control_parameters.panel_control_parameters ):
	def __init__( self, parent, id, pos, size, style ):

		# self.control = control_parameters.Control(self)
		# self.controlshow = control_process_showdata.ShowDataControl(self)
		GUI_control_parameters.panel_control_parameters.__init__(self, parent)
		view_tools.config_control(self, id, pos, size, style)



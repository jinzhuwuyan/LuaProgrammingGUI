"""Subclass of Panel_controlprocess, which is generated by wxFormBuilder."""

import wx
import GUI_controlprocess
from test.control import control_process
from test.control.tools import view_tools
try:
    from wx.lib.pubsub import pub
except ImportError:
    from pubsub import pub
# Implementing Panel_controlprocess
class panel_process( GUI_controlprocess.Panel_controlprocess ):
	def __init__( self, parent, id, pos, size, style ):
		GUI_controlprocess.Panel_controlprocess.__init__( self, parent )
		self.parent = parent
		self.control = control_process.Control(self)
		self.change_status = False
		self.current_func_str = ''
		self.event_list = []
		view_tools.config_control(self, id, pos, size, style)


	# Handlers for Panel_controlprocess events.
	def check_save_status( self, event ):
		self.control.monitor_changes(event, self.change_status)


	def add_functions( self, event ):
		# TODO: Implement add_functions
		self.change_status = True
		self.control.append_item(self.parent.GetParent().panel_functionlist.data.get_selectionstr())
		# self.m_treeControl_show.RefreshItems()
		# self.m_treeControl_show.UnselectAll()

	def delete_functions( self, event ):
		# TODO: Implement delete_functions
		self.change_status = True
		# self.m_dataViewTreeCtrl_show.RemoveChild(self.m_dataViewTreeCtrl_show.GetSelection())
		if self.data.model.items:
			self.control.delete_item()


	def take_function_up( self, event ):
		# TODO: Implement take_function_up
		self.change_status = True
		self.control.change_item_position('up')

	def take_function_down( self, event ):
		# TODO: Implement take_function_down
		self.change_status = True
		self.control.change_item_position('down')

	def save_change( self, event ):
		# TODO: Implement save_change
		self.change_status = False

	def redo_edit( self, event ):
		# TODO: Implement redo_edit
		self.change_status = True
	
	

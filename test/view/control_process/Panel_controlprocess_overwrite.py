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
		self.current_choosen = None
		view_tools.config_control(self, id, pos, size, style)


	# Handlers for Panel_controlprocess events.
	def check_save_status( self, event ):
		self.control.monitor_changes(event, self.change_status)


	def add_functions( self, event ):
		# TODO: Implement add_functions
		self.change_status = True
		self.control.append_item(self.parent.GetParent().panel_functionlist.data.get_selectionstr())


	def delete_functions( self, event ):
		# TODO: Implement delete_functions
		self.change_status = True
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
	
	def refresh_current_selection( self, event ):
		select_item = self.m_treeControl_show.GetSelection()

		if select_item and len(self.m_treeControl_show.GetIndexOfItem(select_item)) > 0:
				items_indexs = self.m_treeControl_show.GetIndexOfItem(select_item)
				if list(items_indexs)[-1] != self.current_choosen:
					print 'refreshing.,...'
					self.current_choosen = list(items_indexs)[-1]
					pub.sendMessage('refresh_paras', data = self.control.get_current_modeldata(), pos = self.control.get_current_pos())
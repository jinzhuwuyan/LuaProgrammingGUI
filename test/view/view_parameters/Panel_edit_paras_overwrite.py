#! encoding: utf-8
import wx
import GUI_control_parameters
from test.control import control_parameters

# Implementing panel_control_paras
class panel_edit_paras( GUI_control_parameters.panel_control_paras ):
	def __init__( self, parent ):
		GUI_control_parameters.panel_control_paras.__init__( self, parent )
		self._control = control_parameters.Control(self)
		self._tmp = None

	# Handlers for panel_control_paras events.
	def check_isNull( self, event ):
		# TODO: Implement check_isNull

		textctrl = event.EventObject
		if not "".join(textctrl.GetValue().split()):
			self._control.set_bitmap('error')
			textctrl.SetValue(self._tmp)
			textctrl.SetFocus()
			wx.MessageBox(u'参数值不能为空！！！')
		else:
			self._control.save_content_from_gui(textctrl.GetValue())

	def save_content( self, event ):
		textctrl = event.EventObject
		if textctrl.GetValue():
			self._control.save_content_from_gui(textctrl.GetValue())

	def save_tmpvalue( self, event ):
		textctrl = event.EventObject
		self._tmp = textctrl.GetValue()
		if not self._tmp:
			self._tmp = '0'
		print self._tmp


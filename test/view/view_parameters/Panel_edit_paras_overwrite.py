#! encoding: utf-8
import wx
import GUI_control_parameters

# Implementing panel_control_paras
class panel_edit_paras( GUI_control_parameters.panel_control_paras ):
	def __init__( self, parent, control, key, value, function_name = None ):
		GUI_control_parameters.panel_control_paras.__init__( self, parent )
		self.parent = parent
		self._control = control
		self._tmp = None
		(ctrl_value, _type) = value
		self.type = _type
		self.function_name = function_name
		print 'init value is %s' % str(value)
		self.m_staticText_paraname.SetLabel(str(key))
		self.m_textCtrl_paravalue.SetValue(str(ctrl_value))
		self._control.set_functionname(self.function_name)

	# Handlers for panel_control_paras events.
	def check_isNull( self, event ):
		# TODO: Implement check_isNull

		textctrl = event.EventObject
		textctrl_value = "".join(textctrl.GetValue().split())
		print 'Checking textctrl value is %s' % textctrl_value
		if self._control.save_content_from_gui(textctrl_value, self.type):
			self.show_msg(u'输入的参数值应该为%s类型' % self.type)

		else:
			self._control.set_bitmap(self.m_bpButton_checkisNull, 'ok')
			self._control.save_content_from_gui(textctrl.GetValue(), self.type)


	def save_content( self, event ):
		textctrl = event.EventObject
		if textctrl.GetValue():
			if not self._control.save_content_from_gui(textctrl.GetValue(), self.type):
				self.show_msg(u'输入的参数值应该为%s类型' % self.type)
		else:
			self._control.set_bitmap(self.m_bpButton_checkisNull, 'error')

	def save_tmpvalue( self, event ):
		self._control.set_bitmap(self.m_bpButton_checkisNull, 'error')
		textctrl = event.EventObject
		self._tmp = textctrl.GetValue()
		if not self._tmp:
			self._tmp = '0'
		# print self._tmp

	def show_msg(self, msg):
		wx.MessageBox(msg)
		self.m_textCtrl_paravalue.SetFocus()
		self.m_textCtrl_paravalue.SetValue(self._tmp)


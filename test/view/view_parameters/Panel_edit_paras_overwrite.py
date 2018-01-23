#! encoding: utf-8
import wx
import GUI_control_parameters

# Implementing panel_control_paras
class panel_edit_paras( GUI_control_parameters.panel_control_paras ):
	def __init__( self, parent, control, key, value ):
		GUI_control_parameters.panel_control_paras.__init__( self, parent )
		self.parent = parent
		self._control = control
		self._tmp = None
		(ctrl_value, _type) = value
		self.type = _type
		# self.function_name = function_name
		self._tmp = str(ctrl_value)
		print 'init value is %s' % str(value)
		self.m_staticText_paraname.SetLabel(str(key))
		self.m_textCtrl_paravalue.SetValue(str(ctrl_value))

		# self._control.set_functionname(self.function_name)

	# Handlers for panel_control_paras events.
	def check_isNull( self, event ):
		# TODO: Implement check_isNull

		textctrl = event.EventObject
		textctrl_value = "".join(textctrl.GetValue().split())
		print 'Checking textctrl value is %s' % textctrl_value
		if self._control.save_content_from_gui(textctrl_value, self.type):
			self._control.set_bitmap(self.m_bpButton_checkisNull, 'ok')
			# self._control.save_content_from_gui(textctrl.GetValue(), self.type)
		else:
			wx.MessageBox(self._control.get_errormsg())
			self.m_textCtrl_paravalue.SetValue(self._tmp)
			# wx.MessageBox(u'输入的参数值应该为%s类型' % self.type)

	# def save_content( self, event ):
	# 	textctrl = event.EventObject
	# 	save_content = textctrl.SetValue(self._tmp)
	# 	if  save_content and self._control.save_content_from_gui(save_content, self.type):
	# 		self._tmp = textctrl.GetValue()
	# 	else:
	# 		# self.show_msg(u'输入的参数值应该为%s类型' % self.type)
	# 		wx.MessageBox(u'输入的参数值应该为%s类型' % self.type)
	# 		textctrl.SetValue(self._tmp)
	# 		# textctrl.SetFocus()
	# 		# self._control.set_bitmap(self.m_bpButton_checkisNull, 'error')

	def save_tmpvalue( self, event ):
		self._control.set_bitmap(self.m_bpButton_checkisNull, 'error')
	# 	# textctrl = event.EventObject
	# 	self._tmp = self.m_textCtrl_paravalue.GetValue()
	# 	if not self._tmp:
	# 		self._tmp = '0'
	# 	print 'Getting tmp value is %s' % self._tmp

	# def show_msg(self, msg):
	# 	wx.MessageBox(msg)
	# 	self.m_textCtrl_paravalue.SetFocus()
	# 	self.m_textCtrl_paravalue.SetValue(self._tmp)


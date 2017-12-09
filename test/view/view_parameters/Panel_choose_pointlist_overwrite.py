#! encoding: utf-8
import sys
import wx
import yaml
import Panel_choose_pointlist
from LuaProgrammingGUI.test.control.control_parameters.control_choose_pointlist import ChoosePoinListControl
from LuaProgrammingGUI.test.control.tools import controlfile_tools

# Implementing Panel_choose_pointlist
class Panel_Choose_Point( Panel_choose_pointlist.choose_pointlist ):
	def __init__( self, parent, filepath, current_selection = 0 ):
		Panel_choose_pointlist.choose_pointlist.__init__( self, parent )
		self.filepath = filepath
		controlfile_tools.log_bystatus("Panel_choose_panel 's path is %s" % self.filepath)
		try:
			with open(self.filepath, 'r') as f:
				data = yaml.load(f.read())
				self.__control = ChoosePoinListControl(self, data)
				ret, ret_msg = self.__control.set_textctrl_datas(current_selection)
				self.m_comboBox_pointlist.SetSelection(current_selection - 1)
				if not ret:
					wx.MessageBox(ret_msg)
		except yaml.YAMLError as e:
			wx.MessageBox('请检查点文件%s是否出现错误！' % self.filepath)
		except Exception as e:
			s = sys.exc_info()
			wx.MessageBox('第%d行初始化维护参数错误！\n错误信息如下,\n%s' % (s[2].tb_lineno, e))

	def choose_point( self, event ):

		if isinstance(event.EventObject, wx.ComboBox):
			value = event.EventObject.GetValue()
			ret_id, ret_idmsg = self.__control.get_id_fromstring(value)
			choose_id = 1
			if ret_id:
				choose_id = ret_idmsg
				ret, ret_msg = self.__control.set_textctrl_datas(choose_id)
			else:
				ret, ret_msg = self.__control.set_textctrl_datas(choose_id)
				wx.MessageBox(ret_idmsg)
			if not ret:
				wx.MessageBox(ret_msg)


	def check_point( self, event ):

		value = self.m_comboBox_pointlist.GetValue()
		ret, ret_msg = self.__control.check_value_availablity(value)
		if not ret:
			wx.MessageBox(ret_msg)
			self.m_comboBox_pointlist.SetSelection(0)
		else:
			# self.m_comboBox_pointlist.SetValue('P-%d' % ret_msg)
			self.m_comboBox_pointlist.SetSelection(ret_msg - 1)
			ret_settext, ret_settext_msg = self.__control.set_textctrl_datas(ret_msg)
			if not ret_settext:
				wx.MessageBox(ret_settext_msg)



if __name__ == '__main__':
	app = wx.App()
	frame = wx.Frame(None)
	panel = Panel_Choose_Point(frame, './test.pts')
	frame.Show(True)
	app.MainLoop()
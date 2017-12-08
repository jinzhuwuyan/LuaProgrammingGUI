#! encoding: utf-8
import wx
import yaml
import Panel_choose_pointlist
from LuaProgrammingGUI.test.control.control_parameters.control_choose_pointlist import ChoosePoinListControl
# Implementing Panel_choose_pointlist
class Panel_Choose_Point( Panel_choose_pointlist.choose_pointlist ):
	def __init__( self, parent ):
		Panel_choose_pointlist.choose_pointlist.__init__( self, parent )
		with open('./test.pts', 'r') as f:
			data = yaml.load(f.read())
		self.__control = ChoosePoinListControl(self, data)
		self.__control.set_textctrl_datas(0)

	def choose_point( self, event ):

		if isinstance(event.EventObject, wx.ComboBox):
			value = event.EventObject.GetValue()
			ret_id, ret_idmsg = self.__control.get_id_fromstring(value)
			if ret_id:
				self.__control.set_textctrl_datas(ret_idmsg - 1)
			else:
				self.__control.set_textctrl_datas(0)
				wx.MessageBox(ret_idmsg)




	def check_point( self, event ):
		print event.EventObject
		value = event.EventObject.GetValue()
		self.__control.check_value_availablity(value)




if __name__ == '__main__':
	app = wx.App()
	frame = wx.Frame(None)
	panel = Panel_Choose_Point(frame)
	frame.Show(True)
	app.MainLoop()
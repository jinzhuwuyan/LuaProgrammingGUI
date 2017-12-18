#! encoding: utf-8
import GUI_functionlist
import os
from LuaProgrammingGUI.test.control.control_function_list import control_function
from LuaProgrammingGUI.test.control.tools import view_tools


# Implementing Panel_ChooseFunc
class Panel_ChooseFunc( GUI_functionlist.Panel_ChooseFunc ):
	def __init__( self, parent, id, pos, size, style ):
		GUI_functionlist.Panel_ChooseFunc.__init__( self, parent )
		self.func_path = None
		self.current_data = None
		self._control = None
		self.config()
		view_tools.config_control(self, id, pos, size, style)

	# Handlers for Panel_ChooseFunc events.
	def update_func( self, event ):
		# TODO: Implement update_func
		self._control.refresh(event.EventObject)

	
	def config(self):
		current_path, _ = os.path.split(__file__)
		self.func_path = os.path.abspath(os.path.join(current_path, '../../control/reference.yml'))
		self._control = control_function.Function_List_Control(self, self.func_path)
		self._control.init_control()
		# 加载函数列表数据
		self.m_listBox_choosefunction.SetItems(self._control.func_paras_keys)




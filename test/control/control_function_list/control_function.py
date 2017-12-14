#!encoding: utf-8
import wx
from LuaProgrammingGUI.test.data.object_function_list import function_object
try:
    from wx.lib.pubsub import pub
except ImportError:
    from pubsub import pub

class Control():

    def __init__(self, parent, func_path = None):

        # function list界面
        self.parent = parent
        # 配置文件路径
        self.reference_path = func_path
        # 树型数据model
        self.model = None
        # 函数参数
        self._funcs_paras = None
        # 配置文件数据
        self._reference_data = None
        # 当前选中的函数
        self._select_obj = None
        # 当前选中的函数位置ID
        self._current_select = None
        # 当前选中的函数名
        self._select_str = None


    def init_control(self):
        self.model = function_object.container()
        # 判断配置文件路径是否为空, 如果为空，不初始化报错，否则初始化数据容器
        if self.reference_path and self.model.init_container(self.reference_path):
            self._funcs_paras = self.model.funcs_data
            self._reference_data = self.model.reference_data
            # 订阅需要返回刷新的函数数据内容
            pub.subscribe(self._send_funcs_data, 'refresh_funcs')
            # process function界面初始化过程中，先发送函数数据
            self._send_funcs_data()
            return True
        else:
            return False

    def get_selection(self):

        return self._current_select

    def get_selectionstr(self):

        return self._select_str

    def get_selectionparas(self):

        _default_para =  {}
        return self._funcs_paras.get(self._select_str, _default_para)

    def get_items_keys(self):

        return self._funcs_paras.keys()

    def get_items_values(self):

        return self._funcs_paras.values()

    def get_items(self):

        return self._funcs_paras

    def _send_funcs_data(self):
        data = (self.get_items(), self.get_selectionstr(), self.get_selection(), self.get_selectionparas(),
                self._reference_data.get('unlimit_func', None), self._reference_data.get('file_path', None),
                self._reference_data.get('rename_list', None), self._reference_data.get('help_msg_path', None))
        pub.sendMessage('refresh_func_ret', data=data)

    def Refresh(self, obj = None):
        """
        refresh the listbox's selection
        :param obj: listbox instance
        :return:
        """
        self._select_obj = obj
        if self._select_obj:
            self._current_select = self._select_obj.GetSelection()
            self._select_str = self._select_obj.GetStringSelection()
            if self._current_select != wx.NOT_FOUND:
                pub.sendMessage('UnSelectAll_controlprocess')
                pub.sendMessage('remove_all_paras')

    def _unselete_all(self):
        for i in range(len(self._select_obj.GetSelections())):
            self._select_obj.Deselect(i)
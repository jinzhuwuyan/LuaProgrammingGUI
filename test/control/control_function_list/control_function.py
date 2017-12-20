#!encoding: utf-8
import wx
from LuaProgrammingGUI.test.data.object_function_list import function_object
try:
    from wx.lib.pubsub import pub
except ImportError:
    from pubsub import pub

class Function_List_Control():

    def __init__(self, parent, func_path = None):

        # function list界面
        self.parent = parent
        # 配置文件路径
        self.reference_path = func_path
        # 数据model
        self.model = None
        # 函数参数
        self._funcs_paras = None
        # 配置文件数据
        self._reference_data = None
        # 当前选中的函数
        self._select_obj = None
        # 当前选中的函数位置
        self._current_select = None
        # 当前选中的函数名
        self._select_str = None

        self.init_control()

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
        else:

            dlg = wx.FileDialog(parent=self.parent, message='加载配置文件有误，请选择一个有效的配置文件！', defaultDir=self.reference_path,
                                wildcard='yml files (*.yml)|*.lts|All files (*.*)|*.*')
            if dlg.ShowModal() == wx.ID_OK:
                self.reference_path = dlg.GetPath()
                self.init_control()
            else:
                wx.MessageBox('初始化界面失败！')
                raise Exception('初始化界面失败！')

    @property
    def func_selection(self):

        return self._current_select

    @property
    def func_str(self):

        return self._select_str

    # @property
    # def func_paras(self):
    #
    #     _default_para =  {}
    #     return self._funcs_paras.get(self._select_str, _default_para)

    @property
    def func_paras_keys(self):

        return self._funcs_paras.keys()

    @property
    def func_paras_values(self):

        return self._funcs_paras.values()

    @property
    def func_paras(self):

        return self._funcs_paras

    @property
    def funcs_hashierarchy(self):

        return self._reference_data.get('unlimit_func', None)

    @property
    def project_file_path(self):
        return self._reference_data.get('file_path', None)

    @property
    def name_reference_list(self):
        return self._reference_data.get('rename_list', None)

    @property
    def help_msg_path(self):
        return self._reference_data.get('help_msg_path', None)


    def _send_funcs_data(self):
        print self.func_paras, self.func_str,
        data = (self.func_paras, self.func_str, self.func_selection,
                self.funcs_hashierarchy, self.project_file_path,
                self.name_reference_list, self.help_msg_path, )
        pub.sendMessage('refresh_func_ret', data=data)

    def refresh(self, obj = None):
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
    #
    # def _unselete_all(self):
    #     for i in range(len(self._select_obj.GetSelections())):
    #         self._select_obj.Deselect(i)
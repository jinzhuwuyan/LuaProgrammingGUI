import wx
from test.data.object_function_list import function_object
try:
    from wx.lib.pubsub import pub
except ImportError:
    from pubsub import pub

class Control():

    def __init__(self, parent, func_path = None):
        self.parent = parent
        self.model = function_object.container(self.parent, func_path)
        self._funcs_paras = self.model.funcs_data
        self._reference_data = self.model.reference_data
        self._select_obj, self._current_select, self._select_str = [None] * 3
        pub.subscribe(self._send_funcs_data, 'refresh_funcs')
        pub.subscribe(self._unselete_all, 'UnSelectAll_funclist')
        self._send_funcs_data()

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
        print '_reference_data is ', self._reference_data
        data = (self.get_items(), self.get_selectionstr(), self.get_selection(), self.get_selectionparas(),
                self._reference_data.get('unlimit_func', None), self._reference_data.get('file_path', None), )
        print 'refresh_func_ret ', data
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
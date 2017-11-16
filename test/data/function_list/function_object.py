from test.control.control_function import Control
class container():
    def __init__(self, func_path = None):

        self._select_obj = None
        self._current_select = 0
        self._select_str = ''
        self._funcs_paras = Control().load_functions(func_path)

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

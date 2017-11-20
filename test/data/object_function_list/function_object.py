import os
from test.control.tools import controlfile_tools as file_control
class container():
    def __init__(self, parent, func_path = None):
        self.parent = parent

        # self._funcs_paras = control_function.Control(self.parent).load_functions(func_path)
        self.funcs_data = self._load_functions(func_path)

    def _load_functions(self, file_path=None):
        if file_path:
                funcs = file_control.loadyaml(file_path)
                if isinstance(funcs, dict):
                    return funcs
                else:
                    file_control.log_bystatus('Please check the content of %s can be loaded by yaml as %s type!!!'
                                              % (file_path, 'dict'), 'e')
                    return self._load_default()
        else:
            return self._load_default()


    def _load_default(self):
        reference_data = file_control.loadyaml(os.path.join(
                os.path.split(os.path.abspath(__file__))[0],
                'reference.yml'))
        _file_path = reference_data['default_func_path']
        _file_name = reference_data['default_func_filename']
        _open_path = os.path.join(_file_path, _file_name)
        _file_data = file_control.loadyaml(_open_path)
        return _file_data

    # def get_selection(self):
    #
    #     return self._current_select
    #
    # def get_selectionstr(self):
    #
    #     return self._select_str
    #
    # # def get_selectionparas(self):
    # #
    # #     _default_para =  {}
    # #     return self._funcs_paras.get(self._select_str, _default_para)
    # #
    # # def get_items_keys(self):
    # #
    # #     return self._funcs_paras.keys()
    # #
    # # def get_items_values(self):
    # #
    # #     return self._funcs_paras.values()
    # #
    # # def get_items(self):
    # #
    # #     return self._funcs_paras

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

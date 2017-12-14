import os
from LuaProgrammingGUI.test.control.tools import controlfile_tools as file_control
class container():
    def __init__(self, parent, func_path = None):
        self.parent = parent

        # self._funcs_paras = control_function.Control(self.parent).load_functions(func_path)
        self.reference_data = None
        self.funcs_data = self._load_functions(func_path)


    def _load_functions(self, file_path=None):

        self.reference_data = file_control.loadyaml(os.path.abspath('./LuaProgrammingGUI/test/control/reference.yml'))
        # self.reference_data = file_control.loadyaml(os.path.abspath('./test/control/reference.yml'))
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
        _file_path = self.reference_data['default_func_path']
        _file_name = self.reference_data['default_func_filename']
        _open_path = os.path.join(_file_path, _file_name)
        _file_data = file_control.loadyaml(_open_path)
        return _file_data


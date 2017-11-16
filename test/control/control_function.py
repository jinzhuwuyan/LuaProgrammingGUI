import os

from tools import controlfile_tools as file_control

class Control():

    def __init__(self):
        pass

    def load_functions(self, file_path=None):
        if file_path:
                funcs = file_control.loadyaml(file_path)
                if isinstance(funcs, dict):
                    return funcs
                else:
                    file_control.log_bystatus('Please check the content of %s can be loaded by yaml as %s type!!!'
                                              % (file_path, 'dict'), 'e')
                    return self.load_default()
        else:
            return self.load_default()


    def load_default(self):
        reference_data = file_control.loadyaml(os.path.join(
                os.path.split(os.path.abspath(__file__))[0],
                'reference.yml'))
        _file_path = reference_data['default_func_path']
        _file_name = reference_data['default_func_filename']
        _open_path = os.path.join(_file_path, _file_name)
        _file_data = file_control.loadyaml(_open_path)
        return _file_data
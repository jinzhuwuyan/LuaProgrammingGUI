#！encoding: utf-8
import os
import yaml
from LuaProgrammingGUI.test.control.tools import controlfile_tools as file_control
class container():
    def __init__(self):

        # 配置数据
        self.reference_data = None
        # 函数列表数据
        self.funcs_data = None

    def init_container(self, func_path):
        """
        初始化数据模型
        :param func_path: 配置路径地址
        :return: True,初始化成功； False,初始化失败
        """
        try:
            with open(func_path, 'r') as f:
                self.reference_data = yaml.load(f.read())
            return self._load_functions(self.reference_data['func_path'])
        except yaml.YAMLError as e:
            print e
            return False
        except Exception as e:
            print e
            return False


    def _load_functions(self, file_path=None):
        """
        加载函数列表
        :param file_path:  函数列表路径
        :return:  True, 加载成功； False, 加载失败
        """

        if file_path:
                self.funcs_data = file_control.loadyaml(file_path)
                return True
        else:
            return False


    # def _load_default(self):
    #     _file_path = self.reference_data['default_func_path']
    #     _file_name = self.reference_data['default_func_filename']
    #     _open_path = os.path.join(_file_path, _file_name)
    #     _file_data = file_control.loadyaml(_open_path)
    #     return _file_data


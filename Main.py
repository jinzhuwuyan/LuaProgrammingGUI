import wx

import os
import sys
current_path, _ = os.path.split(os.path.abspath(__file__))
print current_path, os.path.join(current_path, 'test/'), os.path.join(current_path, 'test/view')
sys.path.insert(0, os.path.abspath(current_path))
sys.path.insert(0, os.path.abspath(os.path.join(current_path, 'test/')))
sys.path.insert(0, os.path.abspath(os.path.join(current_path, 'test/view')))
from control.tools import command_tools
# from test.control.tools import  create_reference
import os
from test.view.MainView import Frame_Main
if __name__ == '__main__':
     app = wx.App()
     Frame_Main(None).Show(True)
     app.MainLoop()
    # print dir(command_tools)
    # print command_tools.__doc__
    # print command_tools.__file__
    # print command_tools.__name__
    # print command_tools.__package__
    # print command_tools.__builtins__
    # type_str = ''
    # for i in dir(command_tools):
    #
    #     exec('print type(command_tools.%s).__name__' % i)
        # if type_str == 'function':
        #     exec('print command_tools.%s.__name__, command_tools.%s.__doc__' % (i, i))
        # if type_str == 'str':
        #     exec('print i')


import wx
from test.view.MainView import Frame_Main
from test.control.tools import  create_reference
import os
if __name__ == '__main__':
    print os.path.abspath('./control')
    app = wx.App()
    Frame_Main(None).Show(True)
    app.MainLoop()
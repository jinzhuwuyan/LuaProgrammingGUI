import wx
from test.view.MainView import Frame_Main
from test.control.tools import  create_reference
if __name__ == '__main__':
    app = wx.App()
    Frame_Main(None).Show(True)
    app.MainLoop()
import wx
from test.view.MainView import Frame_Main
if __name__ == '__main__':
    app = wx.App()
    Frame_Main(None).Show(True)
    app.MainLoop()
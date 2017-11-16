import wx
import Panel_ChooseFunc_overwrite

if __name__ == '__main__':
    app = wx.App()
    frame = wx.Frame(None)
    Panel_ChooseFunc_overwrite.Panel_ChooseFunc(frame)
    frame.Show(True)
    app.MainLoop()


import wx
import Panel_controlprocess_overwrite

if __name__ == '__main__':
    app = wx.App()
    frame = wx.Frame(None)
    Panel_controlprocess_overwrite.panel_process(frame)
    frame.Show(True)
    app.MainLoop()


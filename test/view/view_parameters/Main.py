import wx
import Panel_control_paras_overwrite

if __name__ == '__main__':
    app = wx.App()
    frame = wx.Frame(None)
    Panel_control_paras_overwrite.panel_control_paras(frame)
    frame.Show(True)
    app.MainLoop()


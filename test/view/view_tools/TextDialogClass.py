import wx
import string
class TextDialog(wx.TextEntryDialog):
    def __init__(self, parent, tips_msg, title_msg, default_msg, style, validator=None):
        wx.TextEntryDialog.__init__(self, parent, tips_msg, title_msg, default_msg, style)
        assert isinstance(validator, wx.PyValidator)
        self.SetValidator(validator)
        self.__value = '0'



    def check_OK(self):
        if self.ShowModal() == wx.ID_OK:
            self.__value = self.GetValue() if self.GetValue() != '' else '0'
        self.Show(False)

    def getValue(self):
        return self.__value

class DigitValidator(wx.PyValidator):
    def __init__(self):
        wx.PyValidator.__init__(self)
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def Clone(self):
        return DigitValidator()

    def Validate(self, win):
        tc = self.GetWindow()
        val = tc.GetValue()

        for x in val:
            if x not in string.digits:
                return False

        return True

    def OnChar(self, event):
        key = event.GetKeyCode()

        if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255:
            event.Skip()
            return

        if chr(key) in string.digits:
            event.Skip()
            return

        # Returning without calling even.Skip eats the event before it
        # gets to the text control
        return


class AlphaValidator(wx.PyValidator):
    def __init__(self, ):
        wx.PyValidator.__init__(self)
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def Clone(self):
        return AlphaValidator(self.flag)

    def Validate(self, win):
        tc = self.GetWindow()
        val = tc.GetValue()


        for x in val:
            if x not in string.letters:
                return False
        return True

    def OnChar(self, event):
        key = event.GetKeyCode()

        if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255:
            event.Skip()
            return

        if chr(key) in string.letters:
            event.Skip()
            return

        # Returning without calling even.Skip eats the event before it
        # gets to the text control
        return

if __name__ == '__main__':
    app = wx.App()
    # dlg = TextDialog(None,  'ni shi sb', 'sb', 'sb', wx.OK, DigitValidator())
    # print dlg.check_OK()
    dlg = wx.NumberEntryDialog(None,  'ni shi sb', 'sb', 'aaa', 1, 0, 100)

    dlg.ShowModal()
    app.MainLoop()

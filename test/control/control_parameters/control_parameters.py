import wx
from test.data.object_parameters import parameters_object

class Control():

    def __init__(self, parent):
        self._parent = parent
        self._data = parameters_object.container()

    def save_content_from_gui(self, text_content):
        self.set_bitmap()

    def load_show_content(self, data, pos):
        self._data.model = data
        self._data.pos = pos
        return self._data.get_paras()

    def set_bitmap(self, bitmap_style = 'ok'):
        if bitmap_style == 'ok':
            self._parent.m_bpButton_checkisNull.SetBitmap(wx.ArtProvider.GetBitmap(u"gtk-ok", wx.ART_BUTTON))
        else:
            self._parent.m_bpButton_checkisNull.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_LIST_VIEW, wx.ART_BUTTON))


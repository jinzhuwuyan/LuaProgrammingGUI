import sys
import wx
from LuaProgrammingGUI.test.data.object_process import process_object

class Panel(wx.Panel):
    def __init__(self, *args, **kwargs):
        super(Panel, self).__init__(*args, **kwargs)
        self.data = process_object.container()
        self.log = sys.stdout
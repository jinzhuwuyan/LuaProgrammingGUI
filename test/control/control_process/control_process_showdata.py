#! encoding: utf-8
from LuaProgrammingGUI.test.control.tools import controlfile_tools
from LuaProgrammingGUI.test.data.object_process import process_object

try:
    from wx.lib.pubsub import pub
except ImportError:
    from pubsub import pub

class ShowDataControl():

    def __init__(self, parent):
        # Control.__init__(self, parent)
        self.parent = parent
        self.model = process_object.container()
        pub.subscribe(self.refresh_show_modeldata, 'refresh_show_modeldata')


    def refresh_tree(self):
        self.parent.m_treeControl_showdata.RefreshItems()
        self.parent.m_treeControl_showdata.UnselectAll()

    def translate_modeldata(self, modeldata):
        _tmp = []
        for index, value in enumerate(modeldata):
            (func_str, child, paras) = value
            _tmp.append((str(paras), child, paras))
        return _tmp

    def refresh_show_modeldata(self, data):
        (items, ) = data
        self.model.items = self.translate_modeldata(items)
        controlfile_tools.log_bystatus('Refresh showdata by process control %s ' % str(self.model.items))
        self.refresh_tree()
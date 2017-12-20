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
        self.unlimit_funcs = None
        pub.subscribe(self.refresh_show_modeldata, 'refresh_show_modeldata')
        # pub.subscribe(self._unselete_all, 'unselete_process_all')

    def refresh_tree(self):

        self.parent.m_treeControl_showdata.RefreshItems()
        self.parent.m_treeControl_showdata.UnselectAll()
        # selection = self.parent.m_treeControl_showdata.GetSelection()
        # if  selection \
        #         and self.parent.m_treeControl_showdata.GetItemText(selection, 0) not in self.unlimit_funcs:
        # self.parent.m_treeControl_showdata.UnselectAll()

    # def _unselete_all(self, data):
    #     self.parent.m_treeControl_showdata.UnselectAll()

    def translate_modeldata(self, modeldata):
        _tmp = []
        for index, value in enumerate(modeldata):
            (func_str, child, paras) = value
            if isinstance(paras, dict):
                controlfile_tools.log_bystatus(str([i for i in list(paras.values())]), 'i')
                show_str = ','.join([str(i[0]) for i in list(paras.values())])
                _tmp.append((show_str, child, paras))
        return _tmp

    def refresh_show_modeldata(self, data):
        (items, self.unlimit_funcs) = data
        # self.model.items = self.translate_modeldata(items)
        self.model.items = items
        controlfile_tools.log_bystatus('Refresh showdata by process control %s ' % str(self.model.items))
        self.refresh_tree()
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
**Module Info**::

   @Author     : yan_sw
   @Time       : 2018-01-09 13:53
   @Description:
       control to show current items data

"""
from control.tools import controlfile_tools
from data.object_process import process_object

try:
    from wx.lib.pubsub import pub
except ImportError:
    from pubsub import pub

class ShowDataControl():
    """
                .. admonition:: Class Infos

                        |  *class_description*:
                        |        Control TreeListCtrl data show and refresh
                        |
                        |  *class_chinese_description*:
                        |       控制函数列表树的更新
                        |
                        |
                        | The **initilization** of :class:`~control.control_process.control_process_showdata.ShowDataControl` is:
                        |        control = ShowDataControl(view_instance)``
                        |
                        |
                        | **Parameters of initilization**:
                        |
                        |       **view_instance** : :class:`~view.view_process.Panel_controlprocess_overwrite`  or its subclass
                        |

    """
    def __init__(self, parent):
        # Control.__init__(self, parent)
        self.parent = parent
        self.model = process_object.container()
        self.unlimit_funcs = None
        # 刷新且取消选中
        pub.subscribe(self.refresh_show_modeldata, 'refresh_show_modeldata')
        # 刷新且不取消选中
        pub.subscribe(self.refresh_show_onlyrefreshdata, 'refresh_show_onlyrefreshdata')
        # pub.subscribe(self._unselete_all, 'unselete_process_all')



    def refresh_tree(self):
        """refresh and unselect tree"""
        self.parent.m_treeControl_showdata.RefreshItems()
        self.parent.m_treeControl_showdata.UnselectAll()


    def refresh_show_modeldata(self, data):
        """
        update modeldata of TreeListCtrl as well as unselect Tree

        :param `data`: (itemsdata, condiiton_check_list)
        :type `data`: tuple
        """
        (items, self.unlimit_funcs) = data
        # self.model.items = self.translate_modeldata(items)
        self.model.items = items
        controlfile_tools.log_bystatus('Refresh showdata by process control %s ' % str(self.model.items))
        self.refresh_tree()

    def refresh_show_onlyrefreshdata(self, data):
        """Only refresh modeldata of TreeListCtrl"""
        (items, self.unlimit_funcs) = data
        # self.model.items = self.translate_modeldata(items)
        self.model.items = items
        controlfile_tools.log_bystatus('Refresh showdata by process control %s ' % str(self.model.items))
        self.parent.m_treeControl_showdata.RefreshItems()

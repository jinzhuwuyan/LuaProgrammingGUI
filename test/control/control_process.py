from tools import controlfile_tools

# def check_none(func):
#     def wrapper(*args, **kwargs):
#         (self, event) = args
#         if self.parent == None:
#             deractor_controlfile.log_bystatus('Please init the parent with the type of %s'
#                                               % "<class 'Panel_controlprocess_overwrite.panel_process'>", 'e')
#         else:
#             return func(*args, **kwargs)
#     return wrapper


class Control():

    def __init__(self, parent):
        self.parent = parent

    def monitor_changes(self, event, status):
        event.Enable(status)

    def append_item(self, _panel_process, func_str):
        from test.view.control_process.Panel_controlprocess_overwrite import panel_process

        if isinstance(_panel_process, panel_process):
            _panel_process.change_status = True
            select_item = _panel_process.m_treeControl_show.GetSelection()
            # show_item = _panel_functionlist.data.get_selectionstr()
            controlfile_tools.log_bystatus('select_item is %s' % str(select_item), 'i')
            childitem = _panel_process.data.model.items
            if select_item:
                controlfile_tools.log_bystatus('selection is %s' %
                                               str(_panel_process.m_treeControl_show.GetIndexOfItem(select_item)), 'i')
                select_items = _panel_process.m_treeControl_show.GetIndexOfItem(select_item)
                if len(select_item) == 0:
                    childitem.append((func_str, []))

                elif len(select_items) == 1:

                    (index_1,) = select_items
                    (item_str, itemlist) = childitem[index_1]
                    itemlist.append((func_str, []))
                    childitem[index_1] = (item_str, itemlist)

                elif len(select_items) == 2:
                    (index_1, index_2,) = select_items
                    (item_str, itemlist) = childitem[index_1]
                    (item_str2, itemlist2) = itemlist[index_2]
                    itemlist2.append((func_str, []))
                    itemlist[index_2] = (item_str2, itemlist2)
                    childitem[index_1] = (item_str, itemlist)
                else:
                    controlfile_tools.log_bystatus('select_item_count is %s' % str(len(select_items)), 'i')
                    controlfile_tools.log_bystatus("Can't append out of index 3!", 'e')

            else:
                # 初始化的时候调用此函数添加第一个节点
                childitem.append((func_str, []))

        else:
            controlfile_tools.log_bystatus('Error encounted when updating item, '
                                           'Please check whether panel instance is %s'
                                           % str(panel_process), 'e')




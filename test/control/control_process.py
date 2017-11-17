#! encoding: utf-8
from tools import controlfile_tools

class Control():

    def __init__(self, parent):
        self.parent = parent
        self.func_str, self.func_child, self.command, self.change_way = [None] * 4

    def get_current_pos(self):
        # _pos = []
        # select_item = self.parent.m_treeControl_show.GetSelection()
        # for i in list(self.parent.m_treeControl_show.GetIndexOfItem(select_item)):
        #     _pos.append(i)
        _pos = ['1', '2', '3', '5', 'test']
        return _pos

    def get_current_modeldata(self):
        # 等待重写，只是测试！
        return {'1': {'2': {'3': {'5': {'test': {'X': '1', 'Y': 'ss'}}}, '4': {}}}}

    def monitor_changes(self, event, status):
        event.Enable(status)

    def append_item(self, func_str):
        """控制显示数据"""
        data = (func_str, [])
        self._control_model('add', data)

    def delete_item(self):
        self._control_model('delete')

    def change_item_position(self, change_way = 'up'):
        self.change_way = change_way
        self._control_model('change')

    def _control_model(self, command = 'delete', data = ('', [])):
        controlfile_tools.log_bystatus('Entering control model, data is %s' % str(data), 'i')
        (self.func_str, self.func_child) = data
        self.command = command
        select_item = self.parent.m_treeControl_show.GetSelection()
        # show_item = _panel_functionlist.data.get_selectionstr()
        controlfile_tools.log_bystatus('select_item is %s' % str(select_item), 'i')
        childitem = self.parent.data.model.items

        if select_item:
            controlfile_tools.log_bystatus('selection is %s' %
                                           str(self.parent.m_treeControl_show.GetIndexOfItem(select_item)), 'i')
            select_items = self.parent.m_treeControl_show.GetIndexOfItem(select_item)

            if len(select_items) == 0:
                controlfile_tools.log_bystatus('index is %s' % '0', 'i')
                if self.command == 'add':
                    childitem.append((self.func_str, self.func_child))

            elif len(select_items) == 1:

                (index_1,) = select_items
                controlfile_tools.log_bystatus('index_1 is %s' % str(index_1), 'i')
                childitem = self._control_command(childitem, index_1)

            elif len(select_items) == 2:
                (index_1, index_2,) = select_items
                controlfile_tools.log_bystatus('index_1 is %s, index_2 is %s' % (str(index_1), str(index_2)), 'i')
                (item_str, itemlist) = childitem[index_1]
                itemlist = self._control_command(itemlist, index_2)
                if itemlist:
                    childitem[index_1] = (item_str, itemlist)
            else:
                controlfile_tools.log_bystatus('select_item_count is %s' % str(len(select_items)), 'i')
                controlfile_tools.log_bystatus("Can't append out of index 3!", 'e')

        else:
            # 初始化的时候调用此函数添加第一个节点
            if self.command == 'add':
                childitem.append((self.func_str, self.func_child))
        self.parent.m_treeControl_show.RefreshItems()
        self.parent.m_treeControl_show.UnselectAll()


    def _control_command(self, obj, index):
        (item_str, itemlist) = obj[index]
        controlfile_tools.log_bystatus('index is %s' % str(index), 'i')
        # (item_str, itemlist) = childitem[index_1]
        controlfile_tools.log_bystatus('itemlist is %s' % str(itemlist), 'i')
        if self.command == 'add':
            itemlist.append((self.func_str, self.func_child))
            obj[index] =  (item_str, itemlist)

        elif self.command == 'change':
            move_count = 1
            if self.change_way == 'up' and index > move_count - 1:
                controlfile_tools.log_bystatus('obj[index - 1] = %s, obj[index] = %s' % (str(obj[index - move_count]), str(obj[index])), 'i')
                obj[index - move_count], obj[index] = obj[index], obj[index - move_count]
                controlfile_tools.log_bystatus('obj[index - 1] = %s, obj[index] = %s' % (str(obj[index - move_count]), str(obj[index])), 'i')

            elif self.change_way == 'down' and index < len(obj) - move_count:
                controlfile_tools.log_bystatus('obj[index + 1] = %s, obj[index] = %s' % (str(obj[index + move_count]), str(obj[index])), 'i')
                obj[index + move_count], obj[index] = obj[index], obj[index + move_count]
                controlfile_tools.log_bystatus('obj[index + 1] = %s, obj[index] = %s' % (str(obj[index + move_count]), str(obj[index])), 'i')

            else:
                controlfile_tools.log_bystatus("Can't move the item!", 'e')

        elif self.command == 'delete':
            obj.pop(index)
            obj = None

        return obj


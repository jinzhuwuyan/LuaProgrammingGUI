#! encoding: utf-8
from tools import controlfile_tools
from tools import command_tools
import control_function
try:
    from wx.lib.pubsub import pub
except ImportError:
    from pubsub import pub

class Control():

    def __init__(self, parent):
        self.parent = parent
        self.func_str, self.func_child, self.command, \
            self.change_way, self.func_data, \
            self.func_items, self.func_str, self.func_selection = [None] * 8
        pub.subscribe(self._get_funcs_data, 'refresh_func_ret')


    def refresh_paras_panel(self):
        pub.sendMessage('refresh_paras', data=self.get_current_modeldata(),
                            pos=self.get_current_pos())

    def get_current_pos(self):
        _pos = []
        select_item = self.parent.m_treeControl_show.GetSelection()
        for i in list(self.parent.m_treeControl_show.GetIndexOfItem(select_item)):
            _pos.append(i)
        return _pos

    def get_current_modeldata(self):
        return command_tools.get_dict(self.parent.data.modeldata, self.get_current_pos())

    def update_modeldata(self, data, pos, new_value):

        command_tools.set_dict(data, pos, new_value)

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

    def _control_model(self, command = 'delete', data = ('', [], [])):
        self._refresh_func_init()
        controlfile_tools.log_bystatus('Entering control model, data is %s' % str(data), 'i')
        (self.func_str, self.func_child, self.func_data) = data
        self.command = command
        select_item = self.parent.m_treeControl_show.GetSelection()
        # show_item = _panel_functionlist.data.get_selectionstr()
        controlfile_tools.log_bystatus('select_item is %s' % str(select_item), 'i')
        childitem = self.parent.data.model.items
        # childitemdata = self.parent.data.modeldata
        if select_item:
            controlfile_tools.log_bystatus('selection is %s' %
                                           str(self.parent.m_treeControl_show.GetIndexOfItem(select_item)), 'i')
            select_items = self.parent.m_treeControl_show.GetIndexOfItem(select_item)

            if len(select_items) == 0:
                controlfile_tools.log_bystatus('index is %s' % '0', 'i')
                if self.command == 'add':
                    childitem.append((self.func_str, self.func_child, self.func_data))
                    # childitemdata[self.func_str] = {}

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
                childitem.append((self.func_str, self.func_child, self.func_data))
        self.parent.m_treeControl_show.RefreshItems()
        self.parent.m_treeControl_show.UnselectAll()


    def _control_command(self, obj, index):
        (item_str, itemlist, item_data) = obj[index]
        controlfile_tools.log_bystatus('index is %s' % str(index), 'i')
        # (item_str, itemlist) = childitem[index_1]
        controlfile_tools.log_bystatus('itemlist is %s' % str(itemlist), 'i')
        if self.command == 'add':

            itemlist.append((self.func_str, self.func_child, self.func_data))
            item_data.append((self.func_str, {}))
            obj[index] =  (item_str, itemlist, item_data)


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

    def _refresh_func_init(self):
        pub.sendMessage('refresh_funcs')

    def _get_funcs_data(self, funcs, func_str, func_selection):
        self.func_items = funcs
        self.func_str = func_str
        self.func_selection = func_selection
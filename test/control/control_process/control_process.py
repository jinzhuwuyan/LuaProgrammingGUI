#! encoding: utf-8
from test.control.tools import command_tools
from test.control.tools import controlfile_tools
from test.data.object_process import process_object

try:
    from wx.lib.pubsub import pub
except ImportError:
    from pubsub import pub

class Control():

    def __init__(self, parent):
        self.parent = parent
        self.func_str, self.func_child, self.command, \
            self.change_way, self.func_data, \
            self._func_items, self._func_str, self._func_selection, self._funcs_paras,\
            self.index_1, self.index_2= [None] * 11
        self.model = process_object.container()
        # refresh func data from function list panel
        pub.subscribe(self._get_funcs_data, 'refresh_func_ret')

##########################################control parameters panel#########################################
    def refresh_current_selection(self):
        selection_indexs = self.get_current_pos()
        print 'select_item is ', str(selection_indexs)
        if selection_indexs:
            self.index_1 = selection_indexs[0]
            if len(selection_indexs) > 1:
                self.index_2 = selection_indexs[1]
                print self.model.items
                _, _tmp_item, _ = self.model.items[self.index_1]
                _, _, refresh_data = _tmp_item[self.index_2]
            else:
                print self.model.items
                _, _, refresh_data = self.model.items[self.index_1]
        else:
            refresh_data = {}
        print 'refresh_data ...', refresh_data
        pub.sendMessage('refresh_paras', data=refresh_data,
                            pos=self.get_current_pos())


    def get_current_pos(self):
        _pos = []
        select_item = self.parent.m_treeControl_show.GetSelection()
        if select_item:
            for i in list(self.parent.m_treeControl_show.GetIndexOfItem(select_item)):
                _pos.append(i)
        else:
            # controlfile_tools.log_bystatus("Tree control for showing programming process "
            #                                "don't have selection!", 'e')
            pass
        return _pos


    def update_modeldata(self, data, pos, new_value):

        command_tools.set_dict(data, pos, new_value)



##########################################control programming process panel################################
    def monitor_changes(self, event, status):
        event.Enable(status)

    def append_item(self):
        """控制显示数据"""
        data = (self.get_selectionstr(), [], self.get_selection_paras())
        self._control_model('add', data)

    def delete_item(self):
        self._control_model('delete')

    def change_item_position(self, change_way = 'up'):
        self.change_way = change_way
        self._control_model('change')


    def _control_model(self, command = 'delete', data = ('', [], {})):
        self._refresh_func_init()
        controlfile_tools.log_bystatus('Entering control model, data is %s' % str(data), 'i')
        (self.func_str, self.func_child, self._funcs_paras) = data
        self.command = command
        select_item = self.parent.m_treeControl_show.GetSelection()
        # show_item = _panel_functionlist.data.get_selectionstr()
        controlfile_tools.log_bystatus('select_item is %s' % str(select_item), 'i')
        childitem = self.model.items
        # childitemdata = self.model.modeldata

        if select_item:
            controlfile_tools.log_bystatus('selection is %s' %
                                           str(self.parent.m_treeControl_show.GetIndexOfItem(select_item)), 'i')
            select_items = self.parent.m_treeControl_show.GetIndexOfItem(select_item)

            if len(select_items) == 0:
                controlfile_tools.log_bystatus('index is %s' % '0', 'i')
                if self.command == 'add':
                    childitem.append((self.func_str, self.func_child, self.get_selection_paras()))
                    # childitemdata.append((self.func_str, self.get_funcsitems(), []))
                    # childitemdata[self.func_str] = {}
                    self.index_1, self.index_2 = [None] * 2
            elif len(select_items) == 1:

                (self.index_1,) = select_items
                self.index_2 = None
                controlfile_tools.log_bystatus('index_1 is %s' % str(self.index_1), 'i')
                childitem = self._control_command(childitem, self.index_1)

            elif len(select_items) == 2:
                (self.index_1, self.index_2,) = select_items
                controlfile_tools.log_bystatus('index_1 is %s, index_2 is %s' % (str(self.index_1), str(self.index_2)), 'i')
                (item_str, itemlist) = childitem[self.index_1]

                itemlist = self._control_command(itemlist, self.index_2)
                if itemlist:
                    childitem[self.index_1] = (item_str, itemlist)
            else:
                controlfile_tools.log_bystatus('select_item_count is %s' % str(len(select_items)), 'i')
                controlfile_tools.log_bystatus("Can't append out of index 3!", 'e')

        else:
            # 初始化的时候调用此函数添加第一个节点
            if self.command == 'add':
                childitem.append((self.func_str, self.func_child, self.get_selection_paras()))
                self.index_1, self.index_2 = [None] * 2
                # childitemdata.append((self.func_str, {}, []))
        self.parent.m_treeControl_show.RefreshItems()
        self.parent.m_treeControl_show.UnselectAll()

    def _control_command(self, obj, index):
        (item_str, itemlist, item_data) = obj[index]
        controlfile_tools.log_bystatus('index is %s' % str(index), 'i')
        # (item_str, itemlist) = childitem[index_1]
        controlfile_tools.log_bystatus('itemlist is %s' % str(itemlist), 'i')
        if self.command == 'add':

            itemlist.append((self.func_str, self.func_child, self.get_selection_paras()))
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

##########################################control function list panel################################
    def get_selectionstr(self):
        self._refresh_func_init()
        return self._func_str

    def get_selection(self):
        self._refresh_func_init()
        return self._func_selection

    def get_selection_paras(self):
        return self._funcs_paras

    def get_funcsitems(self):
        self._refresh_func_init()
        return self._func_items

    def _refresh_func_init(self):
        pub.sendMessage('refresh_funcs')

    def _get_funcs_data(self, data):
        (self._func_items, self._func_str, self._func_selection, self._funcs_paras) = data
        print 'recv _get_funcs_data ', data
#! encoding: utf-8
import yaml
import wx
import time
import sys
from LuaProgrammingGUI.test.control.tools import command_tools
from LuaProgrammingGUI.test.control.tools import controlfile_tools
from LuaProgrammingGUI.test.data.object_process import process_object
from LuaProgrammingGUI.test.control.control_process import control_process_showdata
try:
    from wx.lib.pubsub import pub
except ImportError:
    from pubsub import pub

class Control():

    def __init__(self, parent):
        self.version = '.'.join(list('0010'))
        self.parent = parent
        #change
        self.func_str, self.func_child, self.command, \
            self.change_way, self.func_data, \
            self._func_items, self._func_str, self._func_selection, \
            self._funcs_paras, self._funcs_unlimit,\
            self.index_1, self.index_2, self.file_path, \
            self.rename_list= [None] * 14
        self.model = process_object.container()
        self.repeat_time = 1
        # refresh func data from function list panel
        pub.subscribe(self._get_funcs_data, 'refresh_func_ret')
        pub.subscribe(self._refresh_parasdata, 'save_paras')
        pub.subscribe(self._unselete_all, 'UnSelectAll_controlprocess')
        self._refresh_func_init()

##########################################control parameters panel#########################################
    def refresh_current_selection(self):

        refresh_data = self._refresh_parasdata(refresh_type = 'get')
        print 'refresh_data ...', refresh_data
        pub.sendMessage('refresh_paras', data=refresh_data,
                            pos=self.get_current_pos())

    def _refresh_parasdata(self, refresh_type = 'get', data = None):
        print '_refresh_parasdata ', refresh_type, str(data)
        refresh_data = None
        selection_indexs = self.get_current_pos()
        print 'select_item is ', str(selection_indexs)
        if selection_indexs and len(selection_indexs) > 1:
            self.index_1 = selection_indexs[0]
            self.index_2 = selection_indexs[1]
            print self.model.items
            if refresh_type == 'get':
                _, _tmp_item, _ = self.model.items[self.index_1]
                _, _, refresh_data = _tmp_item[self.index_2]
            elif data and refresh_type == 'refresh':
                    _tmp_key1, _tmp_item1, _tmp_paras1 = self.model.items[self.index_1]
                    _tmp_key2, _tmp_item2, refresh_data = _tmp_item1[self.index_2]
                    _tmp_item1[self.index_2] = (_tmp_key2, _tmp_item2, data)
                    self.model.items[self.index_1] = (_tmp_key1, _tmp_item1, _tmp_paras1)
            else:
                controlfile_tools.log_bystatus("Can't check refresh_type or refresh data is None! ", 'e')

        elif selection_indexs and len(selection_indexs) == 1:
            self.index_1 = selection_indexs[0]
            self.index_2 = None
            if refresh_type == 'get':
                _, _, refresh_data = self.model.items[self.index_1]
            elif data and refresh_type == 'refresh':
                controlfile_tools.log_bystatus('refreshing data %s' % str(data))
                _tmp_key1, _tmp_item1, refresh_data = self.model.items[self.index_1]
                self.model.items[self.index_1] = (_tmp_key1, _tmp_item1, data)
            else:
                controlfile_tools.log_bystatus("Can't check refresh_type or refresh data is None! ", 'e')
        else:
            refresh_data = {}

        controlfile_tools.log_bystatus("refresh_type, %s, data, %s, self.model.items,  %s"
                                       % (str(refresh_type), str(data), str(self.model.items)), 'e')
        self.request_showdata_refresh()
        return refresh_data

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

    def modify_runtime(self):
        dlg = wx.NumberEntryDialog(self.parent, '请输入需要循环执行的次数', '次数（默认0为无限循环）：', '输入循环次数弹框', self.repeat_time, 0, 100000)
        if dlg.ShowModal() == wx.ID_OK:
            self.repeat_time = dlg.GetValue()
            wx.MessageBox('设置成功！')
        else:
            print 'Cancle it!'

    def append_item(self):
        """控制显示数据"""
        data = (self.get_selectionstr(), [], self.get_selection_paras())
        self._control_model('add', data)

    def delete_item(self):
        if self.model.items:
            self._control_model('delete')

    def change_item_position(self, change_way = 'up'):
        self.change_way = change_way
        self._control_model('change')

    def save_to_disk(self):
        # TODO: 保存当前数据进行文件
        print 'self.file_path', self.file_path
        if self.file_path:
            try:
                print 'saving file.',self.model.items
                controlfile_tools.save(self.file_path, self.generate_prj_data())
                from LuaProgrammingGUI.demos.luaprogramme.control.Data_Handler import Handle_Msg
                handler = Handle_Msg(self)
                controlfile_tools.log_bystatus(str(self.model.items))
                commands_data = handler.generate_data_from_gui(self.model.items, self.rename_list)
                controlfile_tools.log_bystatus('Generating command data is %s, repeat_time is %d' % (str(commands_data), self.repeat_time))
                handler.generate_commands(commands_data, self.repeat_time)
                controlfile_tools.save(self.file_path+'.lua', handler.output_commands())
                pub.sendMessage('refresh_lua_panel', data = (handler.output_commands(), ))
                return True, '保存成功！'
            except Exception as e:
                exceptions = sys.exc_info()
                return False, '保存失败，请检查第%d行错误原因！' % exceptions[2].tb_lineno
        else:
            # load filepath
            return False, '请检查文件路径%s是否正确？' % self.file_path

    def generate_prj_data(self):
        _tmp = {}
        _tmp['ProgramBlocks'] = self.model.items
        _tmp['Repeat_time'] = self.repeat_time
        _tmp['Last_Edit_time'] = time.asctime( time.localtime(time.time()))
        _tmp['encoding'] = 'utf-8'
        _tmp['Author'] = 'ysw'
        # _tmp['version'] = '.'.join(list('0010'))
        _tmp['version'] = self.version

        return yaml.dump(_tmp)




    def load_from_disk(self):
        # TODO: 从文件中读取数据
        print self.file_path
        if self.file_path:
            filedata = controlfile_tools.loadyaml(self.file_path)
            self.model.items = filedata['ProgramBlocks']
            self.repeat_time = filedata['Repeat_time']
            print 'loading ...', self.model.items
            self.refresh_tree()
        else:
            # load filepath
            pass

    def refresh_tree(self):
        self.request_showdata_refresh()
        self.parent.m_treeControl_show.RefreshItems()
        self.parent.m_treeControl_show.UnselectAll()

    def request_showdata_refresh(self):
        pub.sendMessage('refresh_show_modeldata', data=(self.model.items[:], ))

    def _add_obj_bylimit(self, obj, index, limit = False):

        if not limit:
            (item_str, itemlist, item_data) = obj[index]
            itemlist.append((self.func_str, self.func_child, self.get_selection_paras()))
            obj[index] = (item_str, itemlist, item_data)
        else:
            obj.insert(index + 1, (self.func_str, self.func_child, self.get_selection_paras()))
        print 'Enter by limit is %s' % str(limit)
        return obj

    def _rename_func_str(self, func_str):
        controlfile_tools.log_bystatus('func_str is %s, final_str is %s' % (func_str, self.rename_list[func_str]))
        return self.rename_list[func_str]

    def _change_obj_pos(self, obj, index):
        move_count = 1
        if self.change_way == 'up' and index > move_count - 1:
            controlfile_tools.log_bystatus(
                'obj[index - 1] = %s, obj[index] = %s' % (str(obj[index - move_count]), str(obj[index])), 'i')
            obj[index - move_count], obj[index] = obj[index], obj[index - move_count]
            controlfile_tools.log_bystatus(
                'obj[index - 1] = %s, obj[index] = %s' % (str(obj[index - move_count]), str(obj[index])), 'i')

        elif self.change_way == 'down' and index < len(obj) - move_count:
            controlfile_tools.log_bystatus(
                'obj[index + 1] = %s, obj[index] = %s' % (str(obj[index + move_count]), str(obj[index])), 'i')
            obj[index + move_count], obj[index] = obj[index], obj[index + move_count]
            controlfile_tools.log_bystatus(
                'obj[index + 1] = %s, obj[index] = %s' % (str(obj[index + move_count]), str(obj[index])), 'i')

        else:
            controlfile_tools.log_bystatus("Can't move the item!", 'e')
        return obj

    def _delete_obj(self, obj, index):
        obj.pop(index)
        return None


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
            select_item_str = self.parent.m_treeControl_show.GetItemText(select_item)
            controlfile_tools.log_bystatus('select_items is %s, select_item_str is %s' %
                                           (select_items, select_item_str), 'i')
            if len(select_items) > 2:

                controlfile_tools.log_bystatus('select_item_count is %s' % str(len(select_items)), 'i')
                controlfile_tools.log_bystatus("Can't append out of index 3!", 'e')

            elif len(select_items) == 1:
                (self.index_1,) = select_items
                self.index_2 = None
                controlfile_tools.log_bystatus('index_1 is %s' % str(self.index_1), 'i')
                childitem = self._control_command(childitem, self.index_1, limit=not self._check_func_str(select_item_str))

            elif len(select_items) == 2:

                (self.index_1, self.index_2,) = select_items
                (item_str, itemlist, paraslist) = childitem[self.index_1]
                controlfile_tools.log_bystatus('index_1 is %s, index_2 is %s' % (str(self.index_1), str(self.index_2)), 'i')


                itemlist = self._control_command(itemlist, self.index_2, limit=not self._check_func_str(select_item_str))
                if itemlist:
                    childitem[self.index_1] = (item_str, itemlist, paraslist)
            else:
                controlfile_tools.log_bystatus('index is %s' % '0', 'i')
                if self.command == 'add':
                    childitem.append((self.func_str, self.func_child, self.get_selection_paras()))
                    self.index_1, self.index_2 = [None] * 2


        else:
            # 初始化的时候调用此函数添加第一个节点
            if self.command == 'add':
                childitem.append((self.func_str, self.func_child, self.get_selection_paras()))
                self.index_1, self.index_2 = [None] * 2
                # childitemdata.append((self.func_str, {}, []))
        self.refresh_tree()



    def _control_command(self, obj, index, limit = False):

        if self.command == 'add':
            obj = self._add_obj_bylimit(obj, index, limit=limit)

        elif self.command == 'change':
            obj = self._change_obj_pos(obj, index)

        elif self.command == 'delete':

            obj = self._delete_obj(obj, index)

        return obj


    def _unselete_all(self):
        self.parent.m_treeControl_show.UnselectAll()

    def _check_func_str(self, func_str):
        controlfile_tools.log_bystatus("func_str is %s, _funcs_unlimit is %s" % (str(func_str), str(self._funcs_unlimit)), 'i')
        if func_str in self._funcs_unlimit:
            return True
        else:
            return False

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
        (self._func_items, self._func_str, self._func_selection, self._funcs_paras,
                        self._funcs_unlimit, self.file_path, self.rename_list) = data
        controlfile_tools.log_bystatus('_get_funcs_data is %s' % str(data))
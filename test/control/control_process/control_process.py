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

    def __init__(self, parent, tree=None):
        self.version = '.'.join(list('0010'))
        self.parent = parent
        self.tree = tree
        #change
        self.func_str, self.func_child, self.command, \
            self.change_way, self.func_data, \
            self._func_items, self._func_str, self._func_selection, \
            self._funcs_paras, self._funcs_unlimit,\
            self.index_1, self.index_2, self.file_path, \
            self.rename_list, self.help_msg_path, self.help_msg,\
            self.pos = [None] * 17
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

        refresh_data = None
        selection_indexs = self.get_current_pos()
        controlfile_tools.log_bystatus('_refresh_parasdata %s, data is %s, current_pos is %s' % (str(refresh_type), str(data), str(selection_indexs)))
        # print 'select_item is ', str(selection_indexs)
        if selection_indexs and len(selection_indexs) > 1:
            self.index_1 = selection_indexs[0]
            self.index_2 = selection_indexs[1]
            # print self.model.items
            if refresh_type == 'get':
                _, _tmp_item, _ = self.model.items[self.index_1]
                _, _, refresh_data = _tmp_item[self.index_2]
            elif data and refresh_type == 'refresh':
                    _tmp_key1, _tmp_item1, _tmp_paras1 = self.model.items[self.index_1]
                    _tmp_key2, _tmp_item2, refresh_data = _tmp_item1[self.index_2]
                    _tmp_item1[self.index_2] = (_tmp_key2, _tmp_item2, data)
                    self.model.items[self.index_1] = (_tmp_key1, _tmp_item1, _tmp_paras1)
                    self.request_showdata_refresh()
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
                self.request_showdata_refresh()
            else:
                controlfile_tools.log_bystatus("Can't check refresh_type or refresh data is None! ", 'e')
        else:
            refresh_data = {}

        controlfile_tools.log_bystatus("refresh_type, %s, data, %s, self.model.items,  %s"
                                       % (str(refresh_type), str(data), str(self.model.items)), 'e')

        return refresh_data


    def get_current_pos(self):
        _pos = []
        select_item = self.tree.GetSelection()
        if select_item.m_pItem:
            controlfile_tools.log_bystatus("Enter getpos from get_current_pos")
            for i in list(self.tree.GetIndexOfItem(select_item)):
                _pos.append(i)
        else:
            controlfile_tools.log_bystatus("Tree control for showing programming process "
                                           "don't have selection!")
            pass
        controlfile_tools.log_bystatus('select_item is %s, get_current_pos is %s'
                                       % (str(select_item.m_pItem), str(_pos)))
        return _pos


    def update_modeldata(self, data, pos, new_value):

        command_tools.set_dict(data, pos, new_value)



##########################################control programming process panel################################
    def monitor_changes(self, event, status):
        event.Enable(status)


    def set_tree(self, tree):
        self.tree = tree

    def unselect_items(self):
        controlfile_tools.log_bystatus('UnselectAll items!')
        self.tree.UnselectAll()

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
                commands_data = self.orgnize_commands()
                pub.sendMessage('refresh_lua_panel', data = (commands_data, ))
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

    def orgnize_commands(self):

        from LuaProgrammingGUI.demos.luaprogramme.control.Data_Handler import Handle_Msg
        handler = Handle_Msg(self)
        commands_data = handler.generate_data_from_gui(self.model.items, self.rename_list)
        controlfile_tools.log_bystatus(
            'Generating command data is %s, repeat_time is %d' % (str(commands_data), self.repeat_time))
        head_instance, end_instance = handler.get_repeat_lua_for(self.repeat_time)
        handler.Cmd_Manager.pg.append(head_instance)
        handler.generate_commands(commands_data, self.repeat_time)
        handler.Cmd_Manager.pg.append(end_instance)
        controlfile_tools.save(self.file_path + '.lua', handler.output_commands())
        return handler.output_commands()



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
        # self.parent.m_treeControl_show.RefreshItems()
        controlfile_tools.log_bystatus('refreshing_tree.....')


    def request_showdata_refresh(self):
        controlfile_tools.log_bystatus('show data refresh is %s' % str(self.model.items[:]))
        pub.sendMessage('refresh_show_modeldata', data=(self.model.items[:], self._funcs_unlimit, ))


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
        select_item = self.tree.GetSelection()

        # show_item = _panel_functionlist.data.get_selectionstr()
        controlfile_tools.log_bystatus('select_item is %s' % str(select_item), 'i')
        childitem = self.model.items

        # childitemdata = self.model.modeldata
        try:
            controlfile_tools.log_bystatus('selection is %s' % str(self.tree.GetIndexOfItem(select_item)))
        except Exception as e:
            controlfile_tools.log_bystatus(str(e))
            controlfile_tools.log_bystatus('selection is None')

        if select_item:
            controlfile_tools.log_bystatus('selection is %s' %
                                           str(self.tree.GetIndexOfItem(select_item)), 'i')
            select_items = self.tree.GetIndexOfItem(select_item)
            self.pos = list(select_items)
            select_item_str = self.tree.GetItemText(select_item)
            controlfile_tools.log_bystatus('select_items is %s, select_item_str is %s' %
                                           (select_items, select_item_str), 'i')
            if self.command == 'change':
                controlfile_tools.log_bystatus(
                    'Check Change type is %s' % str(self.check_process_hierarchy(childitem, list(select_items),
                                                                             self.change_way)))
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
                if itemlist and self.command != 'change':
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
            __tmp = []
            parentitem = None
            func_str, child, paras = [None] * 3
            parent_bother_left, parent_bother_right = [None] * 2
            if self.check_process_hierarchy(self.model.items, list(self.pos), self.change_way) == 0:
                obj = self._change_obj_pos(obj, index)
            else:
                if self.change_way == 'up':

                    if index == 0:

                        if self.__set_tree_value_jumpout(self.model.items[:], self.pos, self.change_way):
                            controlfile_tools.log_bystatus('跳转成功！')
                        else:
                            controlfile_tools.log_bystatus('跳转失败！')
                        # for inx, value in enumerate(self.pos):
                        #     if inx + 1 == len(self.pos):
                        #         func_str, child, paras = __tmp[-1]
                        #         if isinstance(child, list):
                        #             child.append(obj[index])
                        #             del obj[index]
                        #         __tmp[-1] = func_str, child, paras
                        #
                        #     else:
                        #         if parentitem:
                        #             parentitem = parentitem[value]
                        #         else:
                        #             parentitem = self.model.items[value]
                        #         __tmp.append(parentitem)
                        # # __tmp.reverse()
                        # while __tmp and len(self.pos) > 1:
                        #     last_one_index = self.pos[-1]
                        #     last_two_index = self.pos[-2]
                        #     # __tmp[last_one_index] = func_str, child, paras
                        #
                        #     func_str_parent, child_parent, paras_parent = __tmp[last_two_index]
                        #     child_parent[last_two_index] = __tmp[last_one_index]
                        #     __tmp[last_two_index] = func_str_parent, child_parent, paras_parent
                        #     self.pos.pop()
                        # lastindex = self.pos.pop()
                        # self.model.items[lastindex] = __tmp[0]
                        # del __tmp[:]
                        # return obj

                    else:
                        (func_str, child, paras) = obj[index - 1]
                        child.append(obj[index])
                        obj[index - 1] = (func_str, child, paras)
                        del obj[index]
                        return obj
                else:
                    if index + 1 == len(obj):
                        if self.__set_tree_value_jumpout(self.model.items[:], self.pos, self.change_way):
                            controlfile_tools.log_bystatus('跳转成功！')
                        else:
                            controlfile_tools.log_bystatus('跳转失败！')
                        # for inx, value in enumerate(self.pos):
                        #     parentitem = self.__get_loop_data(parentitem, value)
                        #     __tmp.append(parentitem)
                        #     if value == self.pos[-1]:
                        #         func_str, child, paras = __tmp[-1]
                        #         del child[index]
                        #         __tmp[-1] = (func_str, child, paras)
                        #         if parent_bother_right:
                        #             _, child_tmp, _ = parent_bother_right
                        #             child_tmp
                        #     elif value == self.pos[-2]:
                        #         _, parentitem_child, _ = __tmp[-2]
                        #
                        #         if 0 < value < len(__tmp[-2]) - 1:
                        #
                        #             parent_bother_left = value - 1
                        #             parent_bother_right = value + 1
                        #         elif value == 0 and len(__tmp[-2]) > 1:
                        #
                        #             parent_bother_left = None
                        #             parent_bother_right = value + 1
                        #         elif value == len(__tmp[-2]) - 1 and len(__tmp[-2]) > 1:
                        #             parent_bother_left = value - 1
                        #             parent_bother_right = None
                        #         else:
                        #             parent_bother_left = None
                        #             parent_bother_right = None
                        #     else:
                        #         pass
                        #
                        # while __tmp and len(self.pos) > 1:
                        #     last_two_index = self.pos[-1]
                        #
                        #     # __tmp[last_one_index] = func_str, child, paras
                        #
                        #     func_str_parent, child_parent, paras_parent = __tmp[-2]
                        #     child_parent[last_two_index] = __tmp[-1]
                        #     __tmp[-2] = func_str_parent, child_parent, paras_parent
                        #     self.pos.pop()
                        # lastindex = self.pos.pop()
                        # self.model.items[lastindex] = __tmp[0]
                        # del __tmp[:]
                        # return obj
                    else:
                        (func_str, child, paras) = obj[index + 1]
                        child.append(obj[index])
                        obj[index + 1] = (func_str, child, paras)
                        del obj[index]
                        return obj


        elif self.command == 'delete':

            obj = self._delete_obj(obj, index)

        return obj

    def __set_tree_value_jumpout(self, treedata, pos, check_type='up'):
        __tmp_data = None
        __tmp = []
        for p in pos:
            __tmp_data = treedata[p] if not __tmp_data else __tmp_data[1][p]
            __tmp.append(__tmp_data)
        setdata = __tmp[-1]
        if len(pos) > 2:
            (func_str_grandfather, func_child_grandfather, func_paras_grandfather) = __tmp[pos[-3]]
            if check_type == 'up':
                func_child_grandfather.insert(pos[-2], setdata)
            else:
                func_child_grandfather.insert(pos[-2] + 1, setdata)
                __tmp[pos[-3]] = (func_str_grandfather, func_child_grandfather, func_paras_grandfather)
        elif len(pos) == 2:
            if check_type == 'up':
                self.model.items.insert(pos[0], setdata)
            else:
                self.model.items.insert(pos[0] + 1, setdata)
        else:
            return False
        del __tmp[-1] # 以便使用parent item来做控制
        delete_pos = pos[-1]
        del __tmp[-1][1][delete_pos]
        # del pos[-1]
        # generate_data = __tmp[::-1]
        # generate_pos = pos[::-1]
        # for inx, p in enumerate(generate_pos):
        #     if inx + 1 < len(generate_pos):
        #         func_str, func_child, func_paras = generate_data[inx+1]
        #         func_child[generate_pos[inx+1]] = generate_data[inx]
        #     else:
        #         self.model.items[p] = generate_data[inx]
        return True

    def __get_loop_data(self, parentitem, index):
        if parentitem:
            parentitem_str, parentitem_child, parentitem_paras = parentitem
            parentitem = parentitem_child[index]
        else:
            parentitem = self.model.items[index]
        return parentitem

    def _check_func_str(self, func_str):
        controlfile_tools.log_bystatus("func_str is %s, _funcs_unlimit is %s" % (str(func_str), str(self._funcs_unlimit)), 'i')
        return func_str in self._funcs_unlimit

    def _unselete_all(self):
        self.tree.UnselectAll()


    ## Addon functions

    def import_prj_fromdisk(self):
        dlg = wx.FileDialog(parent=self.parent, message='Please Choose A project file', defaultDir=self.file_path,
                      wildcard='Lts files (*.lts)|*.lts|All files (*.*)|*.*')
        if dlg.ShowModal() == wx.ID_OK:
            self.file_path = dlg.GetPath()
        else:
            pass
        self.load_from_disk()

    def output_to_folder(self):
        dlg = wx.DirDialog(parent=self.parent, message='Plese Set your path to save project file!',
                           defaultPath=self.file_path, name='view.lts')
        if dlg.ShowModal() == wx.ID_OK:
            self.file_path = dlg.GetPath()
        else:
            pass
        self.save_to_disk()

    def load_help_msg(self):
        controlfile_tools.log_bystatus('help_msg_path is %s' % self.help_msg_path)
        data = controlfile_tools.loadyaml(self.help_msg_path)
        return data

    def get_help(self, func_str):
        return self.help_msg.get(func_str, None)

    def check_process_hierarchy(self, data, pos, check_type='up'):
        """
        return -1 equals to data None or index None.
        return 0  equals to normal change, up is up, down is down.
        return 1 equals to into or outto the hierarchy.
        :param data:
        :param pos:
        :param check_type:
        :return:
        """
        controlfile_tools.log_bystatus('Enter check_process_hierarchy....')
        first_index = pos[0] if pos else None
        _tmp_value = data[first_index] if data else None
        controlfile_tools.log_bystatus('_tmp_value is %s, first_index is %d, data is %s, pos is %s '
                                       % (str(_tmp_value), first_index, str(data), str(pos)))
        if _tmp_value and len(pos) > 1:  # <list>
            del pos[0]
            controlfile_tools.log_bystatus('check_process pos is %s' % str(pos))
            (func_str, child, paras) = _tmp_value
            for index, value in enumerate(pos):  # <list>
                if index + 1 == len(pos):
                    return self.__check_current_func_islimited(child, value, check_type, parentdata=(func_str, child, paras))
                else:
                    try:
                        (func_str, child, paras) = child[value]
                    except Exception:
                        wx.MessageBox('child[value]取值有误， child Is %s' % str(child))
                        return 0
        elif _tmp_value and len(pos) == 1:
            return self.__check_current_func_islimited(data, first_index, check_type, parentdata=None)

        else:
            wx.MessageBox('数据为空！！！')
            return 0

    def __check_current_func_islimited(self, data, index, check_type, parentdata=None):
        """
        考虑到函数自身是否应该上(下)跳或直接移动
        :param data:
        :param index:
        :param check_type:
        :return:
        """
        if 0 < index < len(data) - 1:
            check_value = data[index - 1] if check_type == 'up' else data[index + 1]
            return self.__get_limited_checkvalue(check_value)
        elif index == 0 and len(data) > 1:
            if check_type != 'up':
                check_value = data[index + 1]
                return self.__get_limited_checkvalue(check_value)
            else:
                if parentdata:
                    return 1 if self.__get_limited_checkvalue(parentdata) else 0
                else:
                    return 0
        elif index == len(data) - 1 and len(data) > 1:
            if check_type == 'up':
                check_value = data[index - 1]
                return self.__get_limited_checkvalue(check_value)
            else:
                if parentdata:
                    return self.__get_limited_checkvalue(parentdata)
                else:
                    return 0
        elif len(data) == 1 and parentdata:
            return self.__get_limited_checkvalue(parentdata)

        else:
            return 0


    def __get_limited_checkvalue(self, check_value):

        (func_str_tmp, child, paras) = check_value
        if func_str_tmp in self._funcs_unlimit:
            return 1
        else:
            return 0

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
                        self._funcs_unlimit, self.file_path, self.rename_list, self.help_msg_path) = data
        controlfile_tools.log_bystatus('_get_funcs_data is %s' % str(data))
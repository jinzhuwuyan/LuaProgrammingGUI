#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
**Module Info**::

   @Author     : yan_sw
   @Time       : 2018-01-08 13:53
   @Description:
       This class is the main class for maintaining the treelistctrl data as well as reflect the view event.

"""
import yaml
import wx
import copy
import time
import sys
import os
from control.tools import command_tools
from control.tools import controlfile_tools
from data.object_process import process_object
from control.control_process import control_process_showdata
from control.control_process.TreeItemsControl import TreeItemController
try:
    from wx.lib.pubsub import pub
except ImportError:
    from pubsub import pub

__version__ =  ','.join(list('0010'))

class Control():
    """
                .. admonition:: Class Infos

                        |  *class_description*:
                        |        The core function of controlling the treelistctrl data as well as saving it as a project.
                        |
                        |  *class_chinese_description*:
                        |       刷新当前函数参数面板(:meth:`refresh_current_selection`)
                        |       增加函数(:meth:`control.control_process.TreeItemsControl.control_model`)
                        |       删除函数(:meth:`control.control_process.TreeItemsControl.control_model`)
                        |       改变函数位置(:meth:`control.control_process.TreeItemsControl.control_model`)
                        |       保存(:meth:`save_to_disk`)
                        |       恢复上次操作(:meth:`load_from_disk`)
                        |       修改循环时间(:meth:`modify_runtime`)
                        |       打开工程文件(:meth:`import_prj_fromdisk`)
                        |       另存为工程文件(:meth:`output_to_folder`)
                        |       帮助(:meth:`load_help_msg`)
                        |
                        |
                        | The **initilization** of :class:`~control.control_process.control_process.Control` is:
                        |        control = control.control_process.control_process.Control(view_instance, tree)
                        |
                        |
                        | **Parameters of initilization**:
                        |
                        |       **view_instance** : :class:`~view.view_process.Panel_controlprocess_overwrite`  or its subclass
                        |
                        |
                        |       **tree**: wx.TreeListCtrl
                        |

    """
    def __init__(self, parent, tree=None):
        self.parent = parent
        self.tree = tree
        self.version = None
        self.func_str = None
        self.func_child = None
        self.command = None
        self.change_way = None
        self.func_data = None
        self.func_paras = None
        self.func_items = None
        self.func_selection = None
        self.file_path = None
        self.rename_list = None
        self.help_msg_path = None
        self.help_msg = None
        self.pos = None
        self.model = None
        self.repeat_time = None
        self.file_path_rewrite = None
        self.init_control()


    def init_control(self):
        # change
        self.func_str, self.func_child, self.command, \
        self.change_way, self.func_data, \
        self._func_items, self._func_str, self._func_selection, \
        self._funcs_paras, self._funcs_unlimit, \
        self.index_1, self.index_2, self.file_path, \
        self.rename_list, self.help_msg_path, self.help_msg, \
        self.pos = [None] * 17
        self.model = process_object.container()
        self.repeat_time = 1
        # refresh func data from function list panel
        pub.subscribe(self._get_funcs_data, 'refresh_func_ret')
        pub.subscribe(self._refresh_parasdata, 'save_paras')
        # pub.subscribe(self.refresh_paras_again, 'refresh_paras_again')
        pub.subscribe(self._unselete_all, 'UnSelectAll_controlprocess')
        pub.subscribe(self._rewrite_filepath, 'rewrite_filepath')
        self._refresh_func_init()

##########################################control parameters panel#########################################
    # def refresh_paras_again(self):
    #     controlfile_tools.log_bystatus('refresh again')
    #     self.refresh_current_selection()

    def refresh_current_selection(self):
        """refresh current selected func and func data, show para panel"""
        refresh_data = self._refresh_parasdata(refresh_type = 'get')
        print 'refresh_data ...', refresh_data
        pub.sendMessage('refresh_paras', data=refresh_data,
                            pos=self.get_current_pos())


    def _get_funcs_paras_bypos(self, data, pos):
        """
        get funcs paras from data by pos
        """
        _tmp = None
        for idx, p in enumerate(pos):
            if idx == 0:
                _tmp = data[p]
            else:
                _, child, _ = _tmp
                _tmp = child[p]
        func_str, child, paras = _tmp
        return paras


    def _refresh_item_data(self,  data, pos, refresh_data):
        """generate parent data to refresh according to refresh_data as well as pos """
        _tmp = None
        for idx, p in enumerate(pos):

            if idx == 0:
                _tmp = data[p]
                if len(pos) == 1:
                    func_str, child_tmp, _ = _tmp
                    _tmp = (func_str, child_tmp, refresh_data)
                    data[p] = _tmp
                else:
                    pass
            elif idx + 1 == len(pos):
                controlfile_tools.log_bystatus('_refresh_item_data in last item tmp is %s, refresh_data is %s' % (str(_tmp), str(refresh_data)))
                _, child, _ = _tmp
                controlfile_tools.log_bystatus('_refresh_item_data in last item child is %s' % (str(child)))
                func_str, child_tmp, _ = child[p]
                controlfile_tools.log_bystatus('_refresh_item_data in last item child[p] is %s' % (str(child[p])))
                child[p] = (func_str, child_tmp, refresh_data)
                _tmp = child[p]
                controlfile_tools.log_bystatus('_refresh_item_data in last item tmp is %s, refresh_data is %s' % (str(_tmp), str(refresh_data)))
            else:
                _, child, _ = _tmp
                _tmp = child[p]
        return _tmp




    def replace_freshobj_bypos(self, data, pos, freshobj):
        """
        replace the obj with freshobj according to pos

        :param `data`: items data
        :type `data`: list
        :param `pos`: position of replace obj
        :type `pos`: list
        :param `freshobj`: fresh obj
        :type `freshobj`: tuple
        """
        _tmp = None
        for idx, p in enumerate(pos):

            if idx == 0:
                _tmp = data[p]
                func_str, child_tmp, _= _tmp
                if func_str in self._funcs_unlimit and len(pos) == 1:
                    data[p] = freshobj
                    break
                else:
                    pass

            elif idx + 1 == len(pos):
                _, child, _ = _tmp
                func_str, child_tmp, _ = child[p]
                child[p] = freshobj
            else:
                _, child, _ = _tmp
                _tmp = child[p]

    def _refresh_parasdata(self, refresh_type='get', data=None):
        """refresh or get paras data(`Main Control`)"""
        refresh_data = {}
        selection_indexs = self.get_current_pos()
        controlfile_tools.log_bystatus('_refresh_parasdata %s, data is %s, current_pos is %s' % (
        str(refresh_type), str(data), str(selection_indexs)))
        if selection_indexs:
            if refresh_type == 'get':
                controlfile_tools.log_bystatus('self.model.items is %s' % str(self.model.items))
                refresh_data = self._get_funcs_paras_bypos(self.model.items, selection_indexs)
                controlfile_tools.log_bystatus('refresh_data in _refresh_parasdata is %s' % str(self.model.items))
                return refresh_data
            else:
                # self._refresh_item_data(self.model.items, selection_indexs, data)
                # self.tree.RefreshItems()
                controlfile_tools.log_bystatus('get func_paras by pos is %s' % str(self._get_funcs_paras_bypos(self.model.items, selection_indexs)))
                refresh_obj = self._refresh_item_data(self.model.items, selection_indexs, data)
                controlfile_tools.log_bystatus('get refresh obj is %s' % str(refresh_obj))
                self.replace_freshobj_bypos(self.model.items, selection_indexs, refresh_obj)
                controlfile_tools.log_bystatus('get func_paras by pos is %s' % str(self._get_funcs_paras_bypos(self.model.items, selection_indexs)))
                controlfile_tools.log_bystatus('after refreshing, self.model.items is %s' % str(self.model.items))
                #只刷新数据，不取消选中
                self.request_showdata_onlyrefreshdata()

        else:
            return None




    def get_current_pos(self):
        """get the position according to tree selection"""
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
        """update new_value to data by pos"""
        command_tools.set_dict(data, pos, new_value)



##########################################control programming process panel################################

    def _rewrite_filepath(self, data):
        self.file_path_rewrite = data
        self.load_from_disk()

    def set_tree(self, tree):
        """set process tree"""
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
        self._control_model('delete')

    def change_item_position(self, change_way = 'up'):
            self.change_way = change_way
            self._control_model('change')

    def save_to_disk(self, file_path):
        """save the project data into disk as well as generate commands to lua4 panel"""
        if file_path:
            try:
                print 'saving file.',self.model.items
                if self.model.items:
                    controlfile_tools.save(file_path, self.generate_prj_data())

                    commands_data = self.orgnize_commands(file_path)
                    pub.sendMessage('refresh_lua_panel', data = (commands_data, ))
                    print self.generate_prj_data()
                    # import mm
                    # modelitems = mm.DataModel
                    # modelitems.write('~/Documents/modelitems.xls')
                    return True, '保存成功！'
                else:
                    return False, '为了确保程序正常退出，请至少添加一个延时操作delay!'
            except Exception as e:
                exceptions = sys.exc_info()
                return False, '保存失败，请检查第%d行错误原因！请联系技术人员解决问题！' % exceptions[2].tb_lineno
        else:
            # load filepath
            return False, '请检查文件路径%s是否正确？' % file_path

    def generate_prj_data(self):

        """
        |
        |   Generate the project data of tree model
        |

        .. attention::

               It is neccessary to specific the data structure of project file

               - ProgramBlocks: model data
               - Repeat_time: int
               - Last_Edit_time: time
               - encoding: utf-8
               - Author: ysw
               - version: str


        ..  admonition:: tree model data's data structure


               tree model data ===> [(?), (?), (?), ...]

               ? =====> function str<str>, function child<list>, function paras<dict>

               example:
                   [('if', [], {condition_value: '', operation_value: ''}), ('move', [], {choose_point: (P1, str)}})]
                   there are only one if and move function in this model

                   [('if', [('move', [], {choose_point: (P1, str)})], {condition_value: '', operation_value: ''}), ('move', [], {choose_point: (P1, str)})]
                   this model is different from the one before, because if has its children `move`

               Tips:
                   Only control function like if, while and so on can have child.




        """

        _tmp = {}
        _tmp['ProgramBlocks'] = self.model.items
        _tmp['Repeat_time'] = self.repeat_time
        _tmp['Last_Edit_time'] = time.asctime( time.localtime(time.time()))
        _tmp['encoding'] = 'utf-8'
        _tmp['Author'] = 'ysw'
        # _tmp['version'] = '.'.join(list('0010'))
        _tmp['version'] = self.version

        return yaml.dump(_tmp)

    def orgnize_commands(self, file_path):



        from LuaProgrammingGUI.demos.luaprogramme.control.Data_Handler import Handle_Msg
        handler = Handle_Msg(self)
        commands_data = handler.generate_data_from_gui(self.model.items, self.rename_list)
        controlfile_tools.log_bystatus(
            'generating command data is %s, repeat_time is %d' % (str(commands_data), self.repeat_time))
        head_instance, end_instance = handler.get_repeat_lua_for(self.repeat_time)
        handler.Cmd_Manager.pg.append(head_instance)
        handler.generate_commands(commands_data, self.repeat_time)
        handler.Cmd_Manager.pg.append(end_instance)
        controlfile_tools.save(file_path + '.lua', handler.output_commands())
        return handler.output_commands()


    def load_from_disk(self):
        """load project data with file_path"""
        print self.file_path
        if self.file_path_rewrite:
            filedata = controlfile_tools.loadyaml(self.file_path_rewrite)
            if filedata is None:
                self.model.items = []
            else:
                try:

                    self.model.items = filedata.get('ProgramBlocks', [])
                    self.repeat_time = filedata.get('Repeat_time', 1)
                except KeyError as e:
                    print e
                    wx.MessageBox(u'加载的工程文件不符合格式！请联系技术人员检查工程文件是否损坏！')
                except Exception as e:
                    print e
        elif self.file_path:
            filedata = controlfile_tools.loadyaml(self.file_path)
            self.model.items = filedata['ProgramBlocks']
            self.repeat_time = filedata['Repeat_time']
            print 'loading ...', self.model.items

        else:
            # load filepath
            wx.MessageBox('加载工程文件失败！请选择一个有效的工程进行加载!')

        self.refresh_tree()

    def refresh_tree(self):
        self.request_showdata_refresh()
        # self.parent.m_treeControl_show.RefreshItems()
        controlfile_tools.log_bystatus('refreshing_tree.....')


    def request_showdata_refresh(self):
        """refresh data of treelistctrl as well as unselect all selection"""
        controlfile_tools.log_bystatus('show data refresh is %s' % str(self.model.items[:]))
        pub.sendMessage('refresh_show_modeldata', data=(self.model.items[:], self._funcs_unlimit, ))

    def request_showdata_onlyrefreshdata(self):
        """only refresh data of treelistctrl"""
        controlfile_tools.log_bystatus('show data refresh is %s' % str(self.model.items[:]))
        pub.sendMessage('refresh_show_onlyrefreshdata', data=(self.model.items[:], self._funcs_unlimit, ))



    def _rename_func_str(self, func_str):
        """translate the func str to command str"""
        controlfile_tools.log_bystatus('func_str is %s, final_str is %s' % (func_str, self.rename_list[func_str]))
        return self.rename_list[func_str]


    def _control_model(self, command = 'delete', data = ('', [], {})):
        """main control of controlling the change of data """
        self._refresh_func_init()
        controlfile_tools.log_bystatus('Entering control model, data is %s' % str(data), 'i')
        (self.func_str, self.func_child, self._funcs_paras) = data
        self.command = command
        select_item = self.tree.GetSelection()
        select_items = self.tree.GetIndexOfItem(select_item) if select_item else None
        self.pos = list(select_items) if select_items else None

        self._control_command()
        self.refresh_tree()

    def print_allerrmsg(self, result):
        """print all errmsg if there exists errmsg"""
        for i in result:
            if isinstance(i, list) \
                or isinstance(i, tuple):
                self.print_allerrmsg(i)
            else:
                print unicode(i)

    def _control_command(self):
        """
        truly control function data with command
        """
        if self.command == 'add':
            # obj = self._add_obj_bylimit(obj, index, limit=limit)
            add_control = TreeItemController()
            add_control.config(self.model.items[:], self.pos, self._funcs_unlimit, self.rename_list)
            if self.get_selection_paras():
                self.print_allerrmsg(add_control.control_model(str(self.command), (str(self.func_str), [], self.get_selection_paras())))
                self.model.items = add_control.items
            else:
                wx.MessageBox(u'请选择左侧函数列表中需要添加的函数！')
            # controlfile_tools.log_bystatus('after adding items is %s' % str(self.model.items))
        elif self.command == 'change':
            change_control = TreeItemController()
            change_control.config(self.model.items[:], self.pos, self._funcs_unlimit, self.rename_list)
            if self.pos:
                self.print_allerrmsg(
                    change_control.control_model(str(self.command), (str(self.func_str), [], self.get_selection_paras()), change_way=self.change_way))
                self.model.items = change_control.items
            else:
                wx.MessageBox(u'请选择需要改变位置的函数！')

        elif self.command == 'delete':
            delete_control = TreeItemController()
            delete_control.config(self.model.items[:], self.pos, self._funcs_unlimit, self.rename_list)
            if self.pos:
                self.print_allerrmsg(delete_control.control_model(str(self.command), (str(self.func_str), [], self.get_selection_paras())))
                self.model.items = delete_control.items
            else:
                wx.MessageBox(u'请选择需要删除的函数！')
            # obj = self._delete_obj(obj, index)


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
        controlfile_tools.log_bystatus('_unselect_all items is %s, tree is %s' % (str(self.model.items), str(self.tree)))
        self.tree.RefreshItems()
        self.tree.UnselectAll()


    ## Addon functions

    def import_prj_fromdisk(self):
        """import project data from disk file"""
        dlg = wx.FileDialog(parent=self.parent, message='Please Choose A project file', defaultDir=os.getcwd(),
                      wildcard='Lts files (*.lts)|*.lts|All files (*.*)|*.*')
        if dlg.ShowModal() == wx.ID_OK:
            self.file_path = dlg.GetPath()
            self.load_from_disk()
        else:
            pass


    def output_to_folder(self):
        """save current project data edited on the panel to disk"""
        dlg = wx.FileDialog(
            self.parent, message="请填写需要保存的工程文件名，并选中一个路径进行保存！", defaultDir=os.getcwd(),
            defaultFile="", wildcard='Lts files (*.lts)|*.lts|All files (*.*)|*.*', style=wx.SAVE
        )

        if dlg.ShowModal() == wx.ID_OK:
            self.file_path = dlg.GetPath()
            self.save_to_disk(self.file_path)
        else:
            pass


    def load_help_msg(self):
        """load help msg"""
        controlfile_tools.log_bystatus('help_msg_path is %s' % self.help_msg_path)
        with open(self.help_msg_path, 'r') as f:
            data = unicode(f.read())
            return data

    def get_help(self, func_str):
        return self.help_msg.get(func_str, None)

    def check_process_hierarchy(self, data, pos, check_type='up'):
        """
        check the position whether can be jump out or not

        :param `data`: item data
        :type `data`: list
        :param `pos`: check position
        :type `pos`: list
        :param `check_type`: check up or down
        :rtype: int

        .. attention::

            |
            | return -1 equals to data None or index None.
            | return 0  equals to normal change, up is up, down is down.
            |
            |

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
        print '获取到paras为%s' % str(copy.deepcopy(self._func_items).get(self._func_str, None))
        return copy.deepcopy(self._func_items).get(self._func_str, None)

    def get_funcsitems(self):
        self._refresh_func_init()
        return self._func_items

    def _refresh_func_init(self):
        pub.sendMessage('refresh_funcs')

    def _get_funcs_data(self, data):
        (self._func_items, self._func_str, self._func_selection,
                        self._funcs_unlimit, self.file_path, self.rename_list, self.help_msg_path) = data
        controlfile_tools.log_bystatus('_get_funcs_data is %s' % str(data))

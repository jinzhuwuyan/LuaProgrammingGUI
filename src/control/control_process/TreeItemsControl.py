#! encoding: utf-8
import copy
class TreeItemController():
    def __init__(self):
        self.funcs_unlimit = None
        self.items = None
        self.pos = None
        self.rename_list = None

    def config(self, items, pos, funcs_unlimit, rename_list):
        self.items = items
        self.pos = pos
        self.funcs_unlimit = funcs_unlimit
        self.rename_list = rename_list


########################################################main control##################################
    def control_model(self, command, new_item=None, change_way=None):
            command_funcs_references = {'add': (self._add_obj, (new_item)),
                                        'delete': (self._delete_obj, ()),
                                        'change': (self._change_obj, (change_way))}
            func, paras = command_funcs_references[command]
            funcs_has_paras = ['add', 'change']
            if paras:
                return func(paras) if command in funcs_has_paras \
                                   else (False, u'命令%s参数%s传递错误！！' % (str(command), str(paras)))
            else:
                s = filter(lambda t: t not in funcs_has_paras,
                       command_funcs_references.keys())
                return func() if command in filter(lambda t : t not in funcs_has_paras,
                                                   command_funcs_references.keys()) \
                              else (False, u'命令%s参数%s传递错误！！' % (str(command), str(paras)))


    def _add_obj(self, add_obj):
        if len(add_obj) == 3 \
            and isinstance(add_obj[0], str) \
            and isinstance(add_obj[1], list) \
            and isinstance(add_obj[2], dict):
            parent_item, parent_index = self.get_lastitem(self.pos)
            if parent_item and self.pos:
                index = self.pos[-1]
                func_str, obj_child, _ = parent_item
                try:
                    if not self.__get_limited_checkvalue(parent_item):
                        if parent_index:
                            insert_item, _ = self.get_lastitem(parent_index)
                            _, insert_child, _ = insert_item
                            if index < len(insert_child) - 1:
                                insert_child.insert(index + 1, add_obj)
                            else:
                                insert_child.append(add_obj)
                        else:
                            #不是if同在第一层，就直接插入
                            if index < len(self.items) - 1:
                                self.items.insert(index + 1, add_obj)
                            else:
                                self.items.append(add_obj)
                        # obj_child.append(add_obj)
                    else:

                        obj_child.append(add_obj)

                except IndexError as e:
                    print e
                    print
                    return False, u'无法插入！请检查数据是否能够正确插入'
            elif parent_index == 0:
                self.items.append(add_obj)
            else:
                return False, u'获取位置%s错误，请确保数据存在该位置的数据！' % str(self.pos)
        else:
            return False, u'检查当前添加的对象格式%s, 不符合(str, list, dict)格式' % str(add_obj)

        return True, u'插入成功！'

    def _delete_obj(self):
        obj, parent_index = self.get_lastitem(self.pos)
        _pos = self.pos[:]
        if _pos:
            index = _pos.pop()
            if parent_index and _pos:

                parent_item, _ = self.get_lastitem(_pos)
                if parent_item:
                    _, parent_child, _ = parent_item
                    if index <= len(parent_child) - 1:

                        parent_child.pop(index)
                    else:
                        return False, u'删除位置超范围'
                else:
                    return False, u'当前位置%s不存在！' % str(self.pos)
            else:
                if index <= len(self.items) - 1:
                    self.items.pop(index)
                else:
                    return False, u'删除位置超范围'
        else:
            return False, u'不存在删除位置！'
        return True, u'删除成功！'

    def _change_obj(self, change_way):
        pos = self.pos[:]
        index = pos[-1]
        obj, parent_index = self.get_lastitem(pos)
        check_canjump = self.check_process_hierarchy(self.items, self.pos[:], change_way)
        if check_canjump:
            return self._change_obj_jump(obj, change_way)
        else:
            return self._change_obj_pos(change_way)
########################################################tools control##################################


    def _change_obj_jump(self, obj, change_way):

        _pos1 = self.pos[:]
        _pos1.pop()
        if _pos1:
            parent_item, _ = self.get_lastitem(_pos1)
            _, parent_child, _ = parent_item
        else:
            parent_child = self.items

        index = self.pos[-1]
        # _, obj_child, _ = obj
        if (change_way == 'up' and index == 0) \
            or (change_way == 'down' and index + 1 == len(parent_child)):
                self.__set_tree_value_jumpout(self.items[:], self.pos[:], change_way)
        else:
            _pos = self.pos[:]
            _pos.pop()
            change_index = -1 if change_way == 'up' else 1
            _pos.append(index + change_index)
            parent_item, _ = self.get_lastitem(_pos)
            (func_str, child, paras) = parent_item
            child.append(obj)
            # obj[_pos[-1]] = (func_str, child, paras)
            del parent_child[index]
        return True, u'跳出成功！'

    def get_tree_selection(self):
        # return self.tree.GetIndexOfItem(self.tree.GetSelection())
        return 0

    def get_selection_paras(self):
        return {'test': []}


    def __set_tree_value_jumpout(self, treedata, pos, check_type='up', items=None):
        __tmp_data = None
        __tmp = []
        for p in pos:
            __tmp_data = treedata[p] if not __tmp_data else __tmp_data[1][p]
            __tmp.append(__tmp_data)
        setdata = __tmp[-1]
        if len(pos) > 2:
            (func_str_grandfather, func_child_grandfather, func_paras_grandfather) = __tmp[-3]
            if check_type == 'up':
                func_child_grandfather.insert(pos[-2], setdata)
            else:
                func_child_grandfather.insert(pos[-2] + 1, setdata)
                __tmp[pos[-3]] = (func_str_grandfather, func_child_grandfather, func_paras_grandfather)
        elif len(pos) == 2:
            if check_type == 'up':
                self.items.insert(pos[0], setdata)
            else:
                self.items.insert(pos[0] + 1, setdata)
        else:
            return False
        del __tmp[-1] # 以便使用parent item来做控制
        delete_pos = pos[-1]
        del __tmp[-1][1][delete_pos]

        return True



    def get_lastitem(self, select_items):
        if select_items:
            try:
                _tmp = None
                for idx, pos in enumerate(list(select_items)):
                    if idx == 0:
                        _tmp = self.items[pos]
                    elif idx + 1 == len(select_items):
                        func_str, _, _ = _tmp
                        _, item_child, _ = _tmp
                        _tmp = item_child[pos]

                    else:
                        _, item_child, _ = _tmp
                        _tmp = item_child[pos]
                # 如果是第一层的节点，说明需要直接在第一层内添加，故置为None. 否则取父母的位置出来
                if len(select_items) == 1:
                    parent_index = None
                else:
                    _tmp_pos = select_items[:]
                    _tmp_pos.pop()
                    parent_index = _tmp_pos
                return _tmp, parent_index

            except IndexError as e:
                print e
                return None, -1
        else:
            return None, 0


    def _rename_func_str(self, func_str):
        return self.rename_list[func_str]

    def _change_obj_pos(self, change_way):
        index = self.pos[-1]
        move_count = 1
        _pos = self.pos[:]
        _pos.pop()
        if _pos:
            lastitem, _ = self.get_lastitem(_pos)
            _, obj, _ = lastitem
        else:
            obj = self.items
        if change_way == 'up' and index > move_count - 1:

            obj[index - move_count], obj[index] = obj[index], obj[index - move_count]

        elif change_way == 'down' and index < len(obj) - move_count:

            obj[index + move_count], obj[index] = obj[index], obj[index + move_count]

        else:
            pass
        return True, u'正常切换成功！'

    def __check_current_func_islimited(self, data, index, check_type, parentdata=None):
        """
        考虑到函数自身是否应该上(下)跳或直接移动
        :param data:def _check_func_str(self, func_str):
        return False
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
                    return self.__get_limited_checkvalue(parentdata)
                else:
                    return False
        elif index == len(data) - 1 and len(data) > 1:
            if check_type == 'up':
                check_value = data[index - 1]
                return self.__get_limited_checkvalue(check_value)
            else:
                if parentdata:
                    return self.__get_limited_checkvalue(parentdata)
                else:
                    return False
        elif len(data) == 1 and parentdata:
            return self.__get_limited_checkvalue(parentdata)

        else:
            return False

    def check_process_hierarchy(self, data, pos, check_type='up'):
        """
        return False  equals to normal change, up is up, down is down.
        return True equals to into or outto the hierarchy.
        :param data:
        :param pos:
        :param check_type:
        :return:
        """
        first_index = pos[0] if pos else None
        _tmp_value = data[first_index] if data else None

        if _tmp_value and len(pos) > 1:
            del pos[0]
            (func_str, child, paras) = _tmp_value
            for index, value in enumerate(pos):
                if index + 1 == len(pos):
                    return self.__check_current_func_islimited(child, value, check_type, parentdata=(func_str, child, paras))
                else:
                    try:
                        (func_str, child, paras) = child[value]
                    except Exception:
                        return 0
        elif _tmp_value and len(pos) == 1:
            return self.__check_current_func_islimited(data, first_index, check_type, parentdata=None)

        else:
            return False






    def __get_limited_checkvalue(self, check_value):
        func_str, _, _ = check_value
        return func_str in self.funcs_unlimit




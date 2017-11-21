#! encoding: utf-8
import copy
def get_dict(data, pos):
    """
    按位置获取字典的内容
    :param data: 　dict like {'1': {'2': {'3': {'5': {'test': {'X': '1', 'Y': 'ss'}}}, '4': {}}}}
    :param pos:  list like ['1', '2', '3', '5', 'test']
    :return: obj content
    """
    _obj = data
    for i in pos:
        _obj = _obj.get(i, None)
    return _obj

def set_dict(data, pos, new_value):
    # TODO: change this eval function to tree data structure to avoid eval function uncontrollable.
    eval_str = [ ret_obj('data', pos), ' = ', str(new_value) ]
    eval(''.join(eval_str))
    # TODO: 字符串获取对象怎么做？

    return data


def ret_obj(list_name, obj):
    _ret_list = []
    _tmp = ['[', obj, ']']
    if isinstance(obj, list):
        for i in obj:
            _tmp[1] = i
            _ret_list.extend(_tmp)
    return list_name + ''.join(_ret_list)
#! encoding: utf-8
import copy
import controlfile_tools
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

def check_type(obj, type_str):
    tmp_type = None
    ret = None
    if type_str == 'float' or type_str == str(float):
        tmp_type = float
    elif type_str == 'int' or type_str == str(int):
        tmp_type = int
    elif type_str == 'list' or type_str == str(list):
        tmp_type = list
    elif type_str == 'dict' or type_str == str(dict):
        tmp_type = dict
    elif type_str == 'tuple' or type_str == str(tuple):
        tmp_type = tuple
    elif type_str == 'str' or type_str == str(tuple):
        tmp_type = str
    else:
        controlfile_tools.log_bystatus("Can't check type is %s" % type_str, 'e')
    try:
        ret = tmp_type(obj)
    except Exception as e:
        controlfile_tools.log_bystatus('Error encount when try-catch init %s(%s)'
                                       % (str(obj), str(tmp_type)), 'e')
        ret = None

    return ret

if __name__ == '__main__':
    print check_type(u'6.00', 'float')
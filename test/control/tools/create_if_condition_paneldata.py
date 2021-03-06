#! encoding: utf-8
import yaml
import os
current_path, _ = os.path.split(os.path.abspath(__file__))


conditions = [u'判断输入信号', u'判断输出信号', u'判断位置']
operations = {u'判断输入信号': [u'有信号', u'无信号'], u'判断输出信号': [u'有信号', u'无信号'], u'判断位置': [u'已到达', u'未到达'] }
values = {u'判断输入信号': [unicode(u'端口%d' % in_io) for in_io in range(64)],
          u'判断输出信号': [unicode(u'端口%d' % out_io) for out_io in range(32)],
          u'判断位置': [unicode('P%d' % pos) for pos in range(100)]}
operation_values = {u'有信号': u'==0', u'无信号': u'~=0', u'已到达': u'==0', u'未到达': u'~=0'}
condition_values = {u'输入信号': u'getInput(%s)',
                    u'输出信号': u'getOutput(%s)',
                    u'位置': u'targetOK(%s)'}
default_append_item = (u'判断输入信号', [], {'condition_value': u'0', 'operation_value': u'有信号'})
remove_strs_in_values = [u'端口', u'判断']
default_refresh_data = {'condition': ([], 'list'), 'check_allconditions': True}
condition_data = {}
condition_data['condition'] = conditions
condition_data['operation'] = operations
condition_data['condition_values'] = condition_values
condition_data['operation_values'] = operation_values
condition_data['value'] = values
condition_data['default_append_item'] = default_append_item
condition_data['default_refresh_data'] = default_refresh_data
condition_data['remove_values_msg'] = remove_strs_in_values


IF_CONDITION_PATHS = ['../condition_data.yml', '../../../demos/luaprogramme/command_class/condition_data.yml']

def write_if_condition_values(filepath):

    with open(os.path.abspath(os.path.join(current_path, filepath)), 'w') as f:
        f.write(yaml.dump(condition_data))
        f.close()

for p in IF_CONDITION_PATHS:
    write_if_condition_values(p)


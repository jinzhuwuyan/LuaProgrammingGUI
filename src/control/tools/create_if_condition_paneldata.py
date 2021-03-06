#! encoding: utf-8
import yaml

conditions = [u'判断输入信号', u'判断输出信号', u'判断位置']
operations = {u'判断输入信号': [u'有信号', u'无信号'], u'判断输出信号': [u'有信号', u'无信号'], u'判断位置': [u'已到达', u'未到达'] }
values = {u'判断输入信号': [unicode('getInput(%d)' % in_io) for in_io in range(64)],
          u'判断输出信号': [unicode('getOutput(%d)' % out_io) for out_io in range(32)],
          u'判断位置': [unicode('getTargetOk(P%d)' % pos) for pos in range(100)]}
operation_values = {u'有信号': u'==0', u'无信号': u'!=0', u'已到达': u'==0', u'未到达': u'!=0'}
default_append_item = (u'判断输入信号', [], {'condition_value': u'getInput(0)', 'operation_value': u'有信号'})
default_refresh_data = {'condition': ([], 'list'), 'check_allconditions': True}
condition_data = {}
condition_data['condition'] = conditions
condition_data['operation'] = operations
condition_data['operation_values'] = operation_values
condition_data['value'] = values
condition_data['default_append_item'] = default_append_item
condition_data['default_refresh_data'] = default_refresh_data
with open('../if_condition_data.yml', 'w') as f:
    f.write(yaml.dump(condition_data))
    f.close()


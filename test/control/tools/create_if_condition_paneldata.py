#! encoding: utf-8
import yaml

conditions = [u'判断输入IO', u'判断输出IO', u'判断位置']
operations = {u'判断输入IO': [u'已开启', u'未开启'], u'判断输出IO': [u'已开启1', u'未开启1'], u'判断位置': [u'已到达', u'未到达'] }
values = {u'判断输入IO': [unicode(in_io) for in_io in range(64)],
          u'判断输出IO': [unicode(out_io) for out_io in range(32)],
          u'判断位置': [unicode('P%d' % pos) for pos in range(100)]}
condition_data = {}
condition_data['condition'] = conditions
condition_data['operation'] = operations
condition_data['value'] = values
with open('../if_condition_data.yml', 'w') as f:
    f.write(yaml.dump(condition_data))
    f.close()


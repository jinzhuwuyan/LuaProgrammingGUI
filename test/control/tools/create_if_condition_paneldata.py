import yaml

function_names = [u'输入IO', u'输出IO', u'位置']
function_values = [range(1), {'Point': range(1)}]
function_data = zip(function_names, function_values)

with open('../if_condition_data.yml', 'w') as f:
    f.write(yaml.dump(function_data))
    f.close()


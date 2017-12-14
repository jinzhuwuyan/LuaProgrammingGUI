import os
import yaml
current_path = '.'
create_type = 'reference'
_file_path = ''
_data = ''

print os.path.join(os.path.abspath(current_path))
def get_abspath(reative_path):
    return os.path.abspath(reative_path)
default_coord_data = {'X': (0.00,'float'), 'Y': (0.00, 'float'), 'Z': (0.00, 'float'), 'U': (0.00,'float'), 'V': (0.00, 'float'), 'W': (0.00, 'float')}
default_ja_data = {'J1': (0.00,'float'), 'J2': (0.00, 'float'), 'J3': (0.00, 'float'), 'J4': (0.00,'float'), 'J5': (0.00, 'float'), 'J6': (0.00, 'float')}
default_data = {'value': (0.00, 'float')}
default_condition_data = {'condition': ('', 'str')}
default_none_data = {}
default_time_data = {'time': (0, 'float')}
default_value_data = {'value': (0, 'int')}
default_choose_point_data = {'choose_point': ('P1', 'str')}
funcs = {
    # 'go': default_coord_data,
    # 'move': default_coord_data,
    # 'goja': default_ja_data,
    'GO': default_choose_point_data,
    'MOVE': default_choose_point_data,
    # 'goja': default_ja_data,
    'DELAY': default_time_data,
    'SPEED': default_data,
    'ACCEL': default_data,
    'STOP': default_value_data,
    'ON': default_value_data,
    'OFF': default_value_data,
    # 'if': default_condition_data,
    # 'else': default_none_data,
}
references = {
    'control_path': os.path.join(get_abspath(current_path), '../../control'),
    'data_path': os.path.join(get_abspath(current_path), '../../data'),
    'view_path': os.path.join(get_abspath(current_path), '../../view'),
    'default_func_path': os.path.join(get_abspath(current_path), '../../control'),
    'default_func_filename': 'funcs_data.yml',
    'unlimit_func': ['if', 'else'],
    'file_path': os.path.join(get_abspath(current_path), 'test.lts'),
    'rename_list': {'GO': 'go', 'MOVE': 'move', 'ACCEL': 'setAccel', 'SPEED': 'setSpeed',
                    'DELAY': 'luaSleep', 'STOP': 'emgStop', 'ON': 'on', 'OFF': 'off'}
}


def rewrite_reference():

    _file_path = os.path.join(references['control_path'], 'reference.yml')
    _data = references
    with open(os.path.abspath(_file_path), 'w') as f:
        f.write(yaml.dump(_data))

def rewrite_funcs_data():


    _file_path = os.path.join(references['control_path'], 'funcs_data.yml')
    _data = funcs
    with open(os.path.abspath(_file_path), 'w') as f:
        f.write(yaml.dump(_data))

rewrite_reference()
rewrite_funcs_data()
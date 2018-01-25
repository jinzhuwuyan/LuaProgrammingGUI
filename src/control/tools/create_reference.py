import os
import yaml
current_path, _ = os.path.split(__file__)
create_type = 'reference'
_file_path = ''
_data = ''

print os.path.join(os.path.abspath(current_path))
def get_abspath(reative_path):
    return os.path.abspath(reative_path)

references = {
    'control_path': get_abspath(os.path.join(current_path, '../../control')),
    # 'data_path': os.path.join(get_abspath(current_path), '../../data'),
    # 'view_path': os.path.join(get_abspath(current_path), '../../view'),
    'func_path': get_abspath(os.path.join(current_path, '../../control/funcs_data.yml')),
    # 'default_func_filename': 'funcs_data.yml',
    'unlimit_func': ['IF', 'ELIF', 'ELSE'],
    'file_path': get_abspath(os.path.join(current_path, 'test.lts')),
    'rename_list': {'GO': 'go', 'MOVE': 'move', 'ACCEL': 'setAccel', 'SPEED': 'setSpeed',
                    'DELAY': 'luaSleep', 'STOP': 'emgStop', 'ON': 'on', 'OFF': 'off',
                    'IF': 'if', 'ELSE': 'else', 'ELIF': 'elif'},
    'help_msg_path': get_abspath(os.path.join(current_path, 'help_msg.yml'))
}


def rewrite_reference():

    _file_path = os.path.join(references['control_path'], 'reference.yml')
    _data = references
    with open(os.path.abspath(_file_path), 'w') as f:
        f.write(yaml.dump(_data))


rewrite_reference()

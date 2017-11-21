import os
import yaml
current_path = './test'
create_type = 'reference'
_file_path = ''
_data = ''
def get_abspath(reative_path):
    return os.path.abspath(reative_path)

funcs = {
    'go': {'X': 0, 'Y': 0, 'Z': 0},
    'move': {},

}
references = {
    'control_path': os.path.join(get_abspath(current_path), 'control'),
    'data_path': os.path.join(get_abspath(current_path), 'data'),
    'view_path': os.path.join(get_abspath(current_path), 'view'),
    'default_func_path': os.path.join(get_abspath(current_path), 'control'),
    'default_func_filename': 'funcs_data.yml',


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
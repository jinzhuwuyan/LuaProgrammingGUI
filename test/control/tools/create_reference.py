import os
import yaml
create_type = 'reference'
_file_path = ''
_data = ''
funcs = {
    'go': {'X': 0, 'Y': 0, 'Z': 0},
    'move': {},

}
references = {
    'default_func_path': os.path.abspath('..'),
    'default_func_filename': 'funcs_data.yml',


}
if create_type == 'reference':

    _file_path = '../reference.yml'
    _data = references

elif create_type == 'funcs':

    _file_path = '../funcs_data.yml'
    _data = funcs


with open(os.path.abspath(_file_path), 'w') as f:
    f.write(yaml.dump(_data))
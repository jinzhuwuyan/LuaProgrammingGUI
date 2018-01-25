import yaml
help_data = {
    'GO': 'xxxxxxGo is good!',
    'MOVE': 'xxxxxxxMove is also good!',


}

with open('./help_msg.yml', 'w') as f:
    f.write(yaml.dump(help_data))
    f.close()
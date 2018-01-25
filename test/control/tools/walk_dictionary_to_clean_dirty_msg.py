import os
walk_path = []

def walk_folder(folder_path):
    for f_path, sub_paths, _ in os.walk(folder_path):
        walk_path.append(os.path.abspath(f_path))

        __tmp_paths = [os.path.abspath(os.path.join(f_path, p)) for p in sub_paths]
        if __tmp_paths:
            for sub_path in __tmp_paths:
                walk_folder(sub_path)
        else:
            break

if __name__ == '__main__':

    import commands
    current_path = '/home/pi/Documents/LuaProgrammingGUI'
    dirty_msg = ''
    clean_msg = ''
    clean_object = '*.py'
    walk_folder(current_path)
    for p in walk_path: commands.getstatusoutput('cd %s; sed -i "s/%s/%s/g" ./%s' % (p, dirty_msg, clean_msg, clean_object))
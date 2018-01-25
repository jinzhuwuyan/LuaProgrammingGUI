# TODO LIST
# How can I add an function to the LuaProgramming GUI.
- First I open LuaProgammingGUI/test/control/tools/create_func_data.py, which mainly create function data for function list.
- You will find a dictionary named funcs that there are some existing function.
- You can add the some function in this funcs, for example I will add two functions such as WHILE and FOR to explain how to easily add functions
 to function list.
- 'WHILE': default_condition_data,
  'FOR': for_data,
- You can use the default data like WHILE using the default condition data, as well as, you can identify your data for example FOR
function we see have identify a dictionary, which have a key is 循环次数(大于0次), and the value is a tuple, which the first value is
the key's actual value and the second one is the type of value that it support the basic build-in type in python.

>   #for data
    for_data = {'循环次数(大于0次)': (1, 'int')}
    Tips: The paras panel is a textctrl which need you to specify the number.

- rewrite the docs and add the realization plugin of version choose. ()
#! encoding: utf-8
import wx
import yaml


from demos.luaprogramme.command_class.core import cmds2
from demos.luaprogramme.command_class import CommonCmd


try:
    from wx.lib.pubsub import pub
except ImportError:
    from pubsub import pub

CMD_OBJ_TUPLE = [CommonCmd.Go, CommonCmd.Move, CommonCmd.Sleep, CommonCmd.Stop, CommonCmd.GoJa,
                 CommonCmd.Set_Accel_Go, CommonCmd.Set_Speed_Go, CommonCmd.IF, CommonCmd.ELSE, CommonCmd.FOR, cmds2.End]
CMD_Name_TUPLE = ['go', 'move', 'luaSleep', 'emgStop', 'goja', 'setAccel', 'setSpeed', 'if', 'else', 'for', 'End']
LIMITED_LIST = ['if', 'for']
check_condition = lambda t: t not in LIMITED_LIST
EXEC_CMD_NAMELIST = list(filter(check_condition, CMD_Name_TUPLE))
DATA_DICT_STRS = {'coord': ['go', 'move'],
                  'ja': ['goja'],
                  'time': ['luaSleep'],
                  'value': ['emgStop', 'setAccel', 'setSpeed', 'for'],
                  'condition': ['if'],
                  }
DATA_NONE_LIST = ['else']
class Handle_Msg(object):

    def __init__(self, parent):

        self.parent = parent
        # self.Cmd_Factory = cmds2.CommandManager(CMD_OBJ_TUPLE, CMD_Name_TUPLE, EXEC_CMD_NAMELIST)
        self.Cmd_Factory = CommonCmd.Abstract_CommandManager(CMD_OBJ_TUPLE, CMD_Name_TUPLE, EXEC_CMD_NAMELIST, DATA_NONE_LIST)
        self.Cmd_Manager = cmds2.Prog()
        self.Cmd_data = None # [(func_str, func_paras, func_child_paras), ...]
        self.__end_instances = []

    def output_commands(self):
        # self.Cmd_Manager.printProgramCodes()
        _tmp_str = ''
        print 'output....', self.Cmd_Manager.pg
        self.Cmd_Manager.reorderCodes()
        for line_idx, ln in enumerate(self.Cmd_Manager.pg):  # pgln = program line
            _tmp_str = ''.join([_tmp_str, ln.TabNum * '    ' + ln.genCode(), '\n'])
        return _tmp_str

    def search_data(self, data, deep_list):

        try:
            index = deep_list.pop(0)
            print index
            data_ = data[index]
            print data_
            (_, func_paras, func_child) = data_
            ret_data = self.search_data(func_child, deep_list)
            if ret_data:
                return ret_data
            else:
                return func_paras
        except:
            return None


    def generate_data_from_gui(self, source):

        _tmpchild = []
        func_child_data = None
        for index, obj in enumerate(source):
            (func_str, func_child, func_paras) = obj
            if func_child:
                func_child_data = self.generate_data_from_gui(func_child)
            else:
                func_child_data = []
            _tmpchild.append((func_str, func_paras, func_child_data))
        return _tmpchild

    def get_cmd_paras(self, func_name):
        _check_value = {'coord': list('XYZUVW'), 'ja': list('J1,J2,J3,J4,J5,J6'.split(',')), 'time':['time'],
                        'value': ['value'], 'condition': ['condition']}
        for key, value in  DATA_DICT_STRS.iteritems():
            if func_name in value:
                return _check_value[key]

    def generate_commands(self, commanddata, repeat_time = 1):

        # if self.Gui_data:
        #     command_data = self.generate_data_from_gui(self.Gui_data)
        # print 'Current pg is ', self.Cmd_Manager.pg
        for_head_instance, for_end_instance = self.get_repeat_lua_for(repeat_time)
        self.Cmd_Manager.pg.append(for_head_instance)
        if isinstance(commanddata, list):
            for index, value in enumerate(commanddata):
                (func_str, func_paras, func_child) = value

                if func_str in LIMITED_LIST:

                    # head_instance, end_instance = self.Cmd_Factory.genCmd(str(func_str), func_paras, self.get_cmd_paras(str(func_str)))
                    head_instance, end_instance = self.Cmd_Factory.genCmd_overwrite(str(func_str), func_paras, self.get_cmd_paras(str(func_str)))
                    self.__end_instances.append(end_instance)
                    self.Cmd_Manager.pg.append(head_instance)
                    self.generate_commands(func_child)
                    self.Cmd_Manager.pg.append(self.__end_instances.pop(-1))
                else:
                    print self.Cmd_Factory
                    # instance_exec = self.Cmd_Factory.genCmd(str(func_str))
                    instance_exec = self.Cmd_Factory.genCmd_overwrite(str(func_str), func_paras, self.get_cmd_paras(str(func_str)))
                    self.Cmd_Manager.pg.append(instance_exec)
                print func_paras

        self.Cmd_Manager.pg.append(for_end_instance)
        # print 'self.__end_instances....is ....', self.__end_instances
        # return self.output_commands()
    def get_repeat_lua_for(self, repeat_time):
        head_instance, end_instance = self.Cmd_Factory.genCmd_overwrite('for', {'value': (repeat_time, 'int')},
                                                                        self.get_cmd_paras('for'))
        return head_instance, end_instance



if __name__ == '__main__':

    app = wx.App()
    with open('test.lts', 'r') as f:
        data_tmp = f.read()
        data_gui = yaml.load(data_tmp)
        d = Handle_Msg(None)
        item_command = d.generate_data_from_gui(data_gui)
        print item_command
        # print d.search_data(item_command, [3, 1, 0])
        print d.generate_commands(item_command)

    app.MainLoop()
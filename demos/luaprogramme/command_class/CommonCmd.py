#! encoding: utf-8
from core.cmds2 import Command
from core.cmds2 import CommandManager
try:
    from wx.lib.pubsub import pub
except ImportError:
    from pubsub import pub


class Abstract_CommandManager(CommandManager):

    def __init__(self, cmd_class_tuple, cmd_name_tpl, Exec_cmd_nameList, data_none_list):
        CommandManager.__init__(self, cmd_class_tuple=cmd_class_tuple, cmd_name_tpl=cmd_name_tpl, Exec_cmd_nameList=Exec_cmd_nameList)
        self.__CmdObjTuple = cmd_class_tuple
        self.__CmdList = cmd_name_tpl
        self.__Exec_cmd_nameList = Exec_cmd_nameList
        self.__data_none_list = data_none_list

    def genCmd_overwrite(self, cmdName, data, dict_strs, operation_values = None):
        _tmp = []
        end_cmd = None
        if cmdName in self.__Exec_cmd_nameList:
            cmds = self.genCmd(cmdName=cmdName)
        else:
            cmds,end_cmd = self.genCmd(cmdName=cmdName)

        if cmdName in self.__data_none_list:
            return cmds

        if isinstance(dict_strs, list):
            for key in dict_strs:
                if cmdName == 'if':
                    _tmp.append(data[key])
                else:
                    _tmp.append(data[key][0])
            cmds.data = tuple(_tmp)
            cmds.operations_values = operation_values
        else:
            raise Exception("dict_strs isn't list type!! %s" % (str(dict_strs)))
        if end_cmd:
            return cmds, end_cmd
        else:
            return cmds

    def genCmd_if_condition(self, cmdName, data, dict_strs, check_allconditions):
        cmds, end_cmd = self.genCmd_overwrite(cmdName, data, dict_strs)
        pass

class Abstract_Command(Command):
    def __init__(self, CmdID, commandName, commandType, PairID):

        self.cmdID = CmdID
        self.commandName = commandName
        self.commandType = commandType
        self.PairID = PairID
        Command.__init__(self, cmdID=self.cmdID, commandName=self.commandName, commandType=self.commandType, PairID=self.PairID)
        self.__gen_str = None
        self.__identify_str = str((self.cmdID, self.commandName, self.commandType, self.PairID))
        self.__data = None


    def gen_str(self):
        return ''.join([self.commandName, '(%f, %f, %f, %f, %f, %f)']) #like move(%f, %f, %f, %f, %f, %f)
        # differe from each command.

    @property
    def paradata(self):
        return self.__data

    @paradata.setter
    def data(self, data_content):
        assert isinstance(data_content, tuple)
        self.__data = data_content

    def genCode(self):
        print 'genCode is ', self.gen_str(), self.__data
        return self.gen_str() % self.__data
        # if isinstance(self.data, tuple):
        #     return self.gen_str() % self.data
        # else:
        #     print self.gen_str(), self.data
        #     raise Exception("request_data error, get the data %s from identify %s isn't tuple type" % (str(self.data), self.__identify_str))

class Go(Abstract_Command):

    def __init__(self, CmdID):
        Abstract_Command.__init__(self, CmdID, commandName='go', commandType='EXEC', PairID=None)

    def gen_str(self):
        return ''.join([self.commandName, '(%s)'])


class Move(Abstract_Command):

    def __init__(self, CmdID):
        Abstract_Command.__init__(self, CmdID, commandName='move', commandType='EXEC', PairID=None)

    def gen_str(self):
        return ''.join([self.commandName, '(%s)'])

class GoJa(Abstract_Command):

    def __init__(self, CmdID):
        Abstract_Command.__init__(self, CmdID, commandName='goja', commandType='EXEC', PairID=None)

class Sleep(Abstract_Command):

    def __init__(self, CmdID):
        Abstract_Command.__init__(self, CmdID, commandName='luaSleep', commandType='EXEC', PairID=None)

    def gen_str(self):
        return ''.join([self.commandName, "(%f)"])

class Stop(Abstract_Command):

    def __init__(self, CmdID):
        Abstract_Command.__init__(self, CmdID, commandName='emgStop', commandType='EXEC', PairID=None)

    def gen_str(self):
        return ''.join([self.commandName, "(%d)"])

class Set_Speed_Go(Abstract_Command):

    def __init__(self, CmdID):
        Abstract_Command.__init__(self, CmdID, commandName='setSpeed', commandType='EXEC', PairID=None)

    def gen_str(self):
        return ''.join([self.commandName, "(%d)"])

class Set_Accel_Go(Abstract_Command):

    def __init__(self, CmdID):
        Abstract_Command.__init__(self, CmdID, commandName='setAccel', commandType='EXEC', PairID=None)

    def gen_str(self):
        return ''.join([self.commandName, "(%d)"])

class IF(Abstract_Command):
    def __init__(self, CmdID, inputPairID):
        Abstract_Command.__init__(self, CmdID, commandName='if', commandType='HEAD', PairID=inputPairID)
        self.condition_strs = ''
        self.operations_values = None
        # self.operations_values = {u'有信号': u'==0', u'无信号': u'!=0', u'已到达': u'==0', u'未到达': u'!=0'}

    def generate_if_condition(self):
        print 'generating if condition is ',self.data

    def genCode(self):
        return self.gen_str() % self.condition_strs

    def gen_str(self):
        self.generate_if_condition()
        __condition_values = []
        value, check_allcondition = self.data
        check_str = ' and ' if check_allcondition else ' or '
        if isinstance(value, tuple):
            # value = ([], 'list')
            for condition in value[0]:
                # ([(u'xxx', [], {condition_value: 'xxxx', operation_value: 'xxxx1'})], 'list')
                func_str, _, paras = condition
                condition_str = ''.join([paras['condition_value'], self.operations_values[paras['operation_value']]])
                __condition_values.append(condition_str)
        self.condition_strs = tuple([check_str.join(__condition_values)])


        return ''.join([self.commandName, " (%s) then"])

class ELIF(Abstract_Command):
    def __init__(self, CmdID, inputPairID):
        Abstract_Command.__init__(self, CmdID, commandName='elif', commandType='HEAD', PairID=inputPairID)

    def gen_str(self):
        return ''.join([self.commandName, " (%s) then"])

class ELSE(Command):
    def __init__(self, CmdID):
        Command.__init__(self, CmdID, commandName='else', commandType='HEAD', PairID=None)
        self.commandName = 'else'

    def genCode(self):
        return ''.join([self.commandName, ""])

class FOR(Abstract_Command):
    def __init__(self, CmdID, inputPairID):
        Abstract_Command.__init__(self, CmdID, commandName='for', commandType='HEAD', PairID=inputPairID)

    def gen_str(self):
        return ''.join([self.commandName, " i=0,%d do"])

class WHILE(Abstract_Command):
    def __init__(self, CmdID, inputPairID):
        Abstract_Command.__init__(self, CmdID, commandName='while', commandType='HEAD', PairID=inputPairID)

    def gen_str(self):
        return ''.join([self.commandName, " %s do"])

class ON(Abstract_Command):

    def __init__(self, CmdID):
        Abstract_Command.__init__(self, CmdID, commandName='on', commandType='EXEC', PairID=None)

    def gen_str(self):
        return ''.join([self.commandName, "(%d)"])

class OFF(Abstract_Command):

    def __init__(self, CmdID):
        Abstract_Command.__init__(self, CmdID, commandName='off', commandType='EXEC', PairID=None)

    def gen_str(self):
        return ''.join([self.commandName, "(%d)"])
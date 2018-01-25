
class Command(object):
    def __init__(self,cmdID,commandName,commandType, PairID=None):
        self.TYPES=['HEAD','END','ELSE','EXEC']
        self.__CmdType = ''
        assert commandType in self.TYPES
        self.__setCmdType(commandType)

        assert isinstance(commandName,str)
        self.__CommandName=commandName
        # self.CmdString = ''

        self.__CmdID = cmdID

        print self.__CmdType

        if self.__CmdType !='EXEC':
            assert PairID is not None
        self.__PairID=PairID


        self.InDataDict={}
        self.OutDataDict={}
        self.Condition = ''
        self.TabNum=1





    def getPairID(self):
        return self.__PairID

    def setCondition(self, inputCond):
        self.Condition = inputCond

    def getCmdID(self):
        return self.__CmdID

    # def compoeseCmdString(self):
    #     # output a stringline canbe writen into prog
    #     pass

    def __setCmdType (self, cmdType_input):
        assert cmdType_input in self.TYPES
        self.__CmdType = cmdType_input

    def getCmdType(self):
        return self.__CmdType


    def getCmdName(self):
        return self.__CommandName

    def setInput(self,inputDict):
        self.InDataDict = inputDict

    def getOutput(self):
        return self.OutDataDict

    def getInput(self):
        return self.InDataDict

    def genCode(self):
        # compose in,out data and function to generate python code.
        pass


class Repeat(Command):
    def __init__(self,CmdID,inputPairID):
        Command.__init__(self,CmdID,commandName='Repeat', commandType='HEAD',PairID=inputPairID)
        self.InDataDict = {'RepeatTimes':1}

    def genCode(self):
        # param_N = self.InDataDict['RepeatTimes']
        param_N_str=  str(self.InDataDict['RepeatTimes'])
        code = 'for i in range(' + param_N_str +'):' + '#'+str(self.getPairID())
        return code

class End(Command):
    def __init__(self,CmdID,inputPairID):
        Command.__init__(self,CmdID,commandName='END', commandType='END',PairID=inputPairID)
        self.InDataDict = {'RepeatTimes':1}

    def genCode(self):
        # param_N = self.InDataDict['RepeatTimes']
        code = 'end --#END -- ' + str(self.getPairID())
        return code


class Delay(Command):
    def __init__(self,CmdID):
        Command.__init__(self,CmdID,commandName='Delay', commandType='EXEC',PairID=None)
        self.InDataDict = {'DelaySec':0.5}

    def genCode(self):
        # param_N = self.InDataDict['RepeatTimes']
        param_sec_str=  str(self.InDataDict['DelaySec'])
        code = 'time.sleep(' + param_sec_str +')'
        return code
# ==================# ==================# ==================# ==================# ==================
# ====== every command will be generate from this commandManager and id is unique ======
# ==================# ==================# ==================# ==================# ==================

class CommandManager(object):
    # this is a factory to provide generate object according to give commandLabel
    def __init__(self,cmd_class_tuple,cmd_name_tpl,Exec_cmd_nameList):
        self.__command_id=0
        self.__pair_id = 0
        self.__CmdObjTuple =  cmd_class_tuple
        self.__CmdList = cmd_name_tpl
        self.__Exec_cmd_nameList = Exec_cmd_nameList
        self.CmdReg = dict( zip(self.__CmdList,self.__CmdObjTuple))

        # self.CmdList = ['Click', 'Delay','Move'] +['While','End']
        # self.CmdObjList = [Cmd_Click, Cmd_Delay,Cmd_MoveMouse] +[Cmd_While,Cmd_End]
        # self.CmdDict = dict(zip(self.CmdList,self.CmdObjList))

    def genCmd(self, cmdName):
        # assert cmdName in self.CmdList

        if cmdName in self.__Exec_cmd_nameList:
            print cmdName
            return self.CmdReg[cmdName](self.__genID())
        else:
            this_pID = self.__genPairID()
            head_cmd = self.CmdReg[cmdName](self.__genID(),this_pID)
            end_cmd = self.CmdReg['End'](self.__genID(),this_pID)
            return head_cmd,end_cmd


    def __genID(self):
        self.__command_id += 1
        return self.__command_id

    def __genPairID(self):
        self.__pair_id += 1
        return self.__pair_id


class Prog(object):
    def __init__(self):
        self.pg = [] #programlines
        self.head_idx_list=[]
        self.end_idx_list=[]
        self.PairList = []
        self.PairLevelList = []

    def getTotalLineNum(self):
        return len(self.pg)

    def printProgramCodes(self):
            self.reorderCodes()
            print self.pg
            for line_idx , ln in enumerate(self.pg): #pgln = program line
                print ln.TabNum*'    ' + ln.genCode()

    def __isInPairs(self,idx):
        IsInCell = False
        i = 0
        while not IsInCell:
            cell = self.PairList[i]
            IsInCell = (cell[0] < idx < cell[1])
            i += 1
        return IsInCell

    def reorderCodes(self):
        LastLineTabNum = 1
        self.head_idx_list=[]
        self.end_idx_list=[]
        self.PairList = [] # list of 2-elem-tuple
        self.PairLevelList = [] # pair with list
        self.__scanProgHeadEndPairs()

        TotalLnNum = self.getTotalLineNum()
        level_list = self.__calcPairLevels()
        # level_list = [] if not level_list else level_list
        self.PairLevelList = zip(self.PairList, level_list)

        AllTabNum = [1]* TotalLnNum
        for i in self.PairLevelList:
            pair, level = i
            for j in range(pair[0]+1, pair[1]):
                AllTabNum[j] = level
            AllTabNum[pair[0]] = level - 1
            AllTabNum[pair[1]] = level - 1

        for idx,line_num in enumerate(AllTabNum):
            self.pg[idx].TabNum = line_num


        return 1

    def __calcPairLevels(self):
        TotalPairNum = len(self.PairList)
        if TotalPairNum == 0:
            return None

        PairLenList = [i[1]-i[0] for i in self.PairList]
        Level_list = [2]*len(self.PairList) # the outer(default) is 1, so first loop should be 2
        for idx,p in enumerate(self.PairList):
            L = PairLenList[idx]

            for j, p_j in enumerate(self.PairList):
                L_j = PairLenList[j]
                if L > L_j:
                    IsIn = self.__isPairAInB(p,p_j)
                    if IsIn:
                        Level_list[j] = Level_list[idx]+1
        return Level_list



    def __isPairAInB (self,A,B):
        assert isinstance(A,(list,tuple))
        assert isinstance(B,(list,tuple))
        IsIn = A[0] < B[0] and A[1] > B[1]
        return IsIn



    def __scanOneLineHeadEndPair(self,currentLine,currentLineNum,totalLineNum):
        cur_head_pid = currentLine.getPairID()
        # scan for END which has same pair id with current HEAD
        for idx_j in range(currentLineNum, totalLineNum):
            ln_j = self.pg[idx_j]
            print idx_j, ln_j
            if ln_j.getCmdType() == 'END' and cur_head_pid == ln_j.getPairID():
                pair_head = currentLineNum
                pair_end = idx_j
                return pair_head, pair_end
        return None

    def __scanProgHeadEndPairs(self):
        totalLnNum = len(self.pg)
        for currentLineNum,ln in enumerate(self.pg):
            # scan whole codes
            if ln.getCmdType() == 'HEAD':      # a HEAD sentence
                print ln, currentLineNum, totalLnNum
                pair_head, pair_end = self.__scanOneLineHeadEndPair(ln,currentLineNum,totalLnNum)
                self.head_idx_list.append(pair_head)
                self.end_idx_list.append(pair_end)

        self.PairList = zip(self.head_idx_list,self.end_idx_list)
        IsPairValid = self.chkPair(self.PairList)
        return IsPairValid


    def chkPair (self,PariList):
        # tempList = []
        isinstance(PariList,list)
        N = len(PariList)

        for idx,i in enumerate(PariList):
            tempList = PariList[:]
            tempList.pop(idx)
            cur_pair = i
            for idx_j, j in enumerate(tempList):
                if self.chkCrossPair(cur_pair,j): # crossed happend
                    return False, idx,idx_j
        return True



    def chkCrossPair(self,p1,p2):
        isinstance(p1,tuple or list)
        isinstance(p2,tuple or list)
        if p1[0] < p2[0]:
            UpPair = p1
            DownPair = p2
        else:
            UpPair = p2
            DownPair = p1


        IsCrossed =  DownPair[0] < UpPair[1]  < DownPair[1]
        # print 'UpPair ', UpPair
        # print 'DownPair ', DownPair
        # print IsCrossed

        return IsCrossed



CMD_OBJ_TUPLE = [Repeat,End,Delay]
CMD_Name_TUPLE = ['Repeat','End','Delay']
Exec_cmd_nameList = ['Delay']

if __name__ == '__main__':
    p = Prog()
    cm = CommandManager(CMD_OBJ_TUPLE,CMD_Name_TUPLE,Exec_cmd_nameList)
    c1 = cm.genCmd('Delay')
    p.pg.append(c1)
    c1 = cm.genCmd('Delay')
    p.pg.append(c1)
    c1_,c1e_ = cm.genCmd('Repeat')
    p.pg.insert(0,c1_)

    c3 = cm.genCmd('Delay')
    p.pg.append(c3)
    c3 = cm.genCmd('Delay')
    p.pg.append(c3)



    c1,c1e = cm.genCmd('Repeat')
    p.pg.insert(1,c1)
    p.pg.insert(2,c1e)
    p.pg.append(c1e_)

    # c1,c1e = cm.genCmd('Repeat')
    # p.pg.insert(1,c1)
    # p.pg.insert(6,c1e)
    c3 = cm.genCmd('Delay')
    p.pg.insert(2,c3)

    for i in p.pg:
        print i.getCmdID()
    p.printProgramCodes()
    print p.reorderCodes()
    print p.PairList
    print '========================'
    p.printProgramCodes()
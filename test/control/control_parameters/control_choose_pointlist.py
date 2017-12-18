#! encoding: utf-8
import wx
from LuaProgrammingGUI.test.control.tools import command_tools
from LuaProgrammingGUI.test.control.tools import controlfile_tools
try:
    from wx.lib.pubsub import pub
except ImportError:
    from pubsub import pub

class ChoosePoinListControl():

    def __init__(self, parent, datalist):
        data = (parent, datalist)
        self.init_data(data)
        self.showcontent = {}
        print 'datalists len is %d' % len(datalist)
        controlfile_tools.log_bystatus('Enter ChoosePointListControl')

    def init_data(self, data):
        (parent, datalist, ) = data
        self.parent = parent
        self.datalist = datalist
        self.tc_X, self.tc_Y, self.tc_Z, \
        self.tc_U, self.tc_V, self.tc_W = \
            self.parent.m_textCtrl_Xvalue, self.parent.m_textCtrl_Yvalue, \
            self.parent.m_textCtrl_Zvalue, self.parent.m_textCtrl_Uvalue, \
            self.parent.m_textCtrl_Vvalue, self.parent.m_textCtrl_Wvalue
        # init choose list
        self.set_list_data()
        self.parent.m_comboBox_pointlist.SetSelection(0) if len(self.datalist) > 0 else None

    def set_list_data(self):
        _tmp = []
        for data in self.datalist:
            _tmp.append(''.join(['P-', str(data['Id'])]))
        self.parent.m_comboBox_pointlist.SetItems(_tmp)

    def get_pointbyid(self, id):

        try:
            return  self.datalist[id]
        except Exception as e:
            controlfile_tools.log_bystatus('get_pointbyid is %s' % str(self.datalist))
            print e
            return None

    def set_textctrl_datas(self, id):
        controlfile_tools.log_bystatus('selection id is %d' % id)
        show_point = self.get_pointbyid(id - 1)
        if show_point:
            pos_data = [X, Y, Z, U, V, W] = show_point['Data']
            elbow, handmode = show_point['Elbow'], show_point['Hand']
            tcctrls = [self.tc_X, self.tc_Y, self.tc_Z, self.tc_U, self.tc_V, self.tc_W]
            for index, value in enumerate(tcctrls):
                value.SetValue(str(pos_data[index]))
            self.select_elbow(0 if show_point['Elbow'] == 'A' else 1)
            self.select_handmode(0 if show_point['Hand'] == 'L' else 1)
            # controlfile_tools.log_bystatus('sending save_paras %s' % str(self.showcontent))
            self.showcontent['choose_point'] = ('P%d' % id, 'str')
            pub.sendMessage('save_paras', refresh_type='refresh', data=self.showcontent)

            # pub.sendMessage('save_paras', refresh_type = 'refresh', data = ('P%d' % id, 'str'))
            return True, ''
        else:
            return False, '请检查点文件内容是否有错!'

    def get_id_fromstring(self, value):
        try:
            match_result, match_result_msg = command_tools.re_match(value=value, pattern='P-(\d+)')
            print match_result, match_result_msg, len(self.datalist)
            if match_result:
                id = int(match_result_msg)
                if 0 < id  < len(self.datalist):
                    return True, id
                else:
                    return False, '不存在该点！'
            else:
                return False, '输入有误！'
        except Exception:
            return False, '选择字符串错误！'


    def select_elbow(self, pos):
        self.parent.m_choice_elbow.SetSelection(pos)
        self.parent.m_choice_elbow.Refresh()

    def select_handmode(self, pos):
        self.parent.m_choice_handmode.SetSelection(pos)
        self.parent.m_choice_handmode.Refresh()

    def select_pointlist(self, pos):
        self.parent.m_comboBox_pointlist.SetSelection(pos)
        self.parent.m_comboBox_pointlist.Refresh()

    def check_value_availablity(self, value):
        return self.get_id_fromstring(value)

    def refresh_datalist(self, datalist):
        self.datalist = datalist


#! encoding: utf-8
import wx
class ChoosePoinListControl():

    def __init__(self, parent, datalist):
        data = (parent, datalist)
        self.init_data(data)
        print 'datalists len is %d' % len(datalist)


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
            return None

    def set_textctrl_datas(self, id):
        show_point = self.get_pointbyid(id)
        from LuaProgrammingGUI.test.view.view_tools.FloatSpin import FloatSpinCtrl
        print show_point
        [X, Y, Z, U, V, W] = show_point['Data']
        elbow, handmode = show_point['Elbow'], show_point['Hand']
        self.tc_X.SetValue(str(X))
        self.tc_Y.SetValue(str(Y))
        self.tc_Z.SetValue(str(Z))
        self.tc_U.SetValue(str(U))
        self.tc_V.SetValue(str(V))
        self.tc_W.SetValue(str(W))
        elbowid = 0 if show_point['Elbow'] == 'A' else 1
        handmodeid = 0 if show_point['Hand'] == 'L' else 1
        self.select_elbow(elbowid)
        self.select_handmode(handmodeid)

    def get_id_fromstring(self, value):
        try:
            final_str = value.replace('P', '').replace('-', '')
            print 'final_str is %s' % final_str
            id = int(final_str)
            return True, id

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
        ret, ret_msg = self.get_id_fromstring(value)
        print ret, ret_msg
        if not ret:
            self.select_pointlist(0)
            wx.MessageBox(ret_msg)
        else:
            pass

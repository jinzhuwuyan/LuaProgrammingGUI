#! encoding: utf-8
"""
**Module Info**::

   Author: yan_sw
   Date: 2018-01-08 13:53
   Description:
       Control the para panel which need to choose a point as an paras value

"""
import wx
import os
import yaml
from control.tools import command_tools
from control.tools import controlfile_tools
try:
    from wx.lib.pubsub import pub
except ImportError:
    from pubsub import pub

class ChoosePoinListControl():
    """
            .. admonition:: Class Description

                    |   Class for which function need to choose a point as parameter and show the detailed information of
                    | chosen point. When a point have been chosen, it ought to update the paras data.
                    |
                    | 此类用于维护函数的参数点数据更新及被选中的点数据的显示(:meth:`set_textctrl_datas`)
                    |
                    |
                    | The **initilization** of :class:`ChoosePointListControl` is:
                    |        ``control = ChoosePointListControl(view_instance, datalist)``
                    |
                    |
                    | **Parameters of initilization**:
                    |
                    |       **view_instance** : :class:`~view.view_parameters.Panel_choose_pointlist_overwrite`  or its subclass
                    |           A view instance with a combo box
                    |
                    |       **datalist** : list
                    |           A data list which is loaded from a pts file with yaml type

    """
    def __init__(self, parent, datalist):
        # X_value textCtrl to show
        self.tc_X = None
        # Y_value textCtrl to show
        self.tc_Y = None
        # Z_value textCtrl to show
        self.tc_Z = None
        # U_value textCtrl to show
        self.tc_U = None
        # V_value textCtrl to show
        self.tc_V = None
        # W_value textCtrl to show
        self.tc_W = None

        self.parent = None
        # datalist for initing point list
        self.datalist = None
        # an comboBox
        self.pointchooseBox = None
        # the data for refreshing
        self.showcontent = {}

        self.init_data((parent, datalist))

    def init_data(self, data):
        """init data"""
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
        """init the point data for comboxBox"""
        _tmp = []
        for data in self.datalist:
            _tmp.append(''.join(['P-', str(data['Id'])]))
        self.parent.m_comboBox_pointlist.SetItems(_tmp)

    def get_pointbyid(self, id):
        """return the point by comboBox selection"""
        try:
            return  self.datalist[id]
        except Exception as e:
            controlfile_tools.log_bystatus('get_pointbyid is %s' % str(self.datalist))
            print e
            return None

    def init_textctrl_datas(self, id):

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

    def set_textctrl_datas(self, id):
        """
        set the point data to these value TextCtrl by comboBox selection
        :param `id`: the combox id
        :type `id`: int

        :rtype: tuple



        .. attention::

                | The return format is (isFunctionTargetOk, showmsg)
                | if isFunctionTargetOk is False, then will show the showmsg

        """
        point_templatedata = None
        point_template_yamldata = None
        controlfile_tools.log_bystatus('selection id is %d' % id)
        point_template_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'point_template.yml')
        with open(point_template_filepath, 'r') as f:
            point_templatedata = f.read()
            point_template_yamldata = yaml.load(point_templatedata)
        show_point = self.get_pointbyid(id - 1)
        if point_templatedata and point_template_yamldata:
            pass
        else:
            return False, '用于检查点有效性的点文件模板没有内容！请检查%s路径下的点文件模板是否正常！' % str(point_template_filepath)
        if show_point:
            pos_data = [X, Y, Z, U, V, W] = show_point['Data']
            elbow, handmode = show_point['Elbow'], show_point['Hand']
            if pos_data == point_template_yamldata['Data'] \
                and elbow == point_template_yamldata['Elbow'] \
                and handmode == point_template_yamldata['Hand']:
                wx.MessageBox('当前选中的点不存在数据！请检查是否选择错误！')
            return self.init_textctrl_datas(id)

        else:
            return False, '请检查点文件内容是否有错!'

    def get_id_fromstring(self, value):
        """Get the selection from comboBox value"""
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
        """refresh elbow value of the point data"""
        self.parent.m_choice_elbow.SetSelection(pos)
        self.parent.m_choice_elbow.Refresh()

    def select_handmode(self, pos):
        """refresh the handmode value of the point data"""
        self.parent.m_choice_handmode.SetSelection(pos)
        self.parent.m_choice_handmode.Refresh()

    def select_pointlist(self, pos):
        """refresh the selection of the pointlist"""
        self.parent.m_comboBox_pointlist.SetSelection(pos)
        self.parent.m_comboBox_pointlist.Refresh()

    def check_value_availablity(self, value):
        """return id if the comboBox value is correct"""
        return self.get_id_fromstring(value)

    def refresh_datalist(self, datalist):
        """ refresh datalist which have been initilized"""
        self.datalist = datalist


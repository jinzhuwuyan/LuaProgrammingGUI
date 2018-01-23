#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
**Module Info**::

   @Author     : yan_sw
   @Time       : 2018-01-09 09:03
   @Description:
         This class is main control of paras control.
         It have realized the basic function of maintaining paras data.

"""
import copy
import wx
import yaml
from data.object_parameters import parameters_object
from control.tools import command_tools
from control.tools import controlfile_tools
from view.view_parameters import Panel_edit_paras_overwrite
from view.view_parameters import Panel_choose_pointlist_overwrite
from view.view_parameters import Panel_edit_if_condition_overwrite
try:
    from wx.lib.pubsub import pub
except ImportError:
    from pubsub import pub


class Control():
    """
                .. admonition:: Class Infos

                        |  *class_description*:
                        |        control to maintain basic condition which don't have specific panel to choose
                        |
                        |  *class_chinese_description*:
                        |        根据不同的参数类型选择不同的参数界面(:meth:`refresh_paraslist`)
                        |
                        |
                        | The **initilization** of :class:`~condition.control_parameters.control_parameters.Control` is:
                        |        control = (view_instance, pts_path)
                        |
                        |
                        | **Parameters of initilization**:
                        |
                        |       **view_instance** : :class:`~view.view_parameters.Panel_edit_paras_overwrite`  or its subclass
                        |
                        |       **pts_path**:  str
                        |               point file path
                        |

    """
    def __init__(self, parent, pts_path = None):
        self._parent = parent
        self.pts_path = pts_path
        self.model = parameters_object.container()
        self.controllist = {}
        self.function_name = None
        self.if_conditiondata_path = None
        self.check_value = None
        self.check_value_msg = None
        self.init_control()
        pub.subscribe(self.refresh_paras_panel1, 'refresh_paras')
        pub.subscribe(self._remove_allcontrols, 'remove_all_paras')
        pub.subscribe(self._get_MainMsg, 'get_main_msg')

    #
    # def unselete_process_all(self):
    #     pub.sendMessage('unselete_process_all', data = ())
    def init_control(self):
        self.check_value = {'SPEED': self.check_speed_or_accel_value,
                            'ACCEL': self.check_speed_or_accel_value,
                            'DELAY': self.check_naturalnumber_value,
                            'ON':  self.check_io_value,
                            'OFF': self.check_io_value,
                            'FOR': self.check_naturalnumber_value,
                            }
        self.check_value_msg = {'SPEED': u'速度必须在0到100之间！',
                                'ACCEL': u'加速度必须在0到100之间！',
                                'DELAY': u'等待时间必须大于0！',
                                'ON': u'开启输出信号必须在0到31之间！',
                                'OFF': u'关闭输出信号必须在0到31之间！',
                                'FOR': u'FOR的循环次数必须大于0!',
                                }

    def save_content_from_gui(self, text_content, _type):
        """
        save textctrl value to control process

        :param `text_content`:  textctrl value
        :type `text_content`: str
        :param `_type`: traslate type
        :type `_type`: str

        .. attention::

            |   _type is the type for checking whether text_context can be translated
            |
            |   if the value can't be translated, then return False
            |
        """

        controlfile_tools.log_bystatus('text_content is %s, type is %s' % (text_content, _type), 'i')
        save_data = command_tools.check_type(text_content, _type)
        controlfile_tools.log_bystatus('save_data is %s' % save_data, 'i')
        if save_data and self.check_functionlimits(self.function_name, save_data):

                self.request_save_data()
                controlfile_tools.log_bystatus('request saving data %s' % save_data, 'i')
                return True
        else:
            return False


    def request_save_data(self):
        _check = False
        controlfile_tools.log_bystatus('self.controllist -->%s' % self.controllist)
        if  self.model.showcontent:
            showdata = copy.deepcopy(self.model.showcontent)
            for key, values in showdata.iteritems():
                panel = self.controllist.get(key, None)
                if panel != None:
                    text_content = panel.m_textCtrl_paravalue.GetValue()
                    text_type = panel.type
                    print text_type, type(text_content), text_content
                    value = command_tools.check_type(text_content, text_type)
                    if value != None:
                        showdata[key] = (value, text_type)
                        _check = True
                    else:
                        controlfile_tools.log_bystatus('Save content error!, Please check the value %s, '
                                                       'and type %s are correct!' % (text_content, text_type), 'e')
                        _check = False
                        break
                else:
                    controlfile_tools.log_bystatus('Panel got to save is None', 'e')
            if _check:
                controlfile_tools.log_bystatus("send pub.sendMessage save_paras "
                                               "refresh_type is %s, data is %s" % ('refresh', showdata), 'w')
                pub.sendMessage('save_paras', refresh_type = 'refresh', data = showdata)
            else:
                controlfile_tools.log_bystatus("check is false, Don't send paras to synchronize", 'w')
        else:
            controlfile_tools.log_bystatus("showcontent of panel is None", 'w')

    def load_show_content(self, data, pos):
        """get the function paras data with pos from data"""
        self.model.model = data
        self.model.pos = pos
        return self.model.get_paras()

    def set_bitmap(self, btn_obj, bitmap_style = 'ok'):
        if bitmap_style == 'ok':
            btn_obj.SetBitmap(wx.ArtProvider.GetBitmap(u"gtk-ok", wx.ART_BUTTON))
        else:
            btn_obj.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_LIST_VIEW, wx.ART_BUTTON))

    def refresh_paras_panel1(self, data):
        """
        refresh paras panel

        :param data: para data
        :param pos:  not used
        """
        # TODO: Implement refresh_paras_panel
        # show_content = self.control.load_show_content( data, pos )
        controlfile_tools.log_bystatus('Entering refresh_paras_panel1... %s' % str(data) )
        self.controllist.clear()
        self._remove_allcontrols()
        ##-----------------------init value------------------
        reorder_list = [list('XYZUVW'), 'J1,J2,J3,J4,J5,J6'.split(',')]
        self.model.showcontent, self.function_name = data
        print 'data is ', self.model.showcontent, '.......'
        sizer = self._parent.GetSizer()
        #-------------------Logic-----------------
        if self.model.showcontent:
            check_list = self.model.showcontent.keys()
            for check in reorder_list:
                if check_list[0] in check:
                    check_list = check
                    break
                else:
                    continue
            controlfile_tools.log_bystatus('keys is .....%s' % str(check_list), 'i')

            self.refresh_paraslist(check_list)

            controlfile_tools.log_bystatus("Find %d controls to layout, data str is %s"
                                           % (len(data), data), 'i')

        else:
            controlfile_tools.log_bystatus("Don't have any control to refresh!", 'e')
        sizer.Layout()

    def refresh_paraslist(self, check_list):
        """
        refresh paras panel with check list

        :param `check_list`:  paras keys
        :type `check_list`: dict

        .. attention::

            |   check_list == {'choose_point': ????} ----> :class:`view.view_parameters.Panel_choose_pointlist_overwrite`
            |
            |   check_list == {'condition': ????, .....} ----> :class:`view.view_parameters.Panel_edit_if_condition_overwrite`
            |
            |   check_list == {.....} ----> :class:`view.view_parameters.Panel_edit_paras_overwrite`

        """
        controlfile_tools.log_bystatus('check_list is %s ' % str(check_list))

        if len(check_list) == 1 and 'choose_point' in check_list:
            key = check_list[0]
            id_str = (self.model.showcontent[key][0]).replace('P', '')
            id = int(id_str)
            controlfile_tools.log_bystatus('refreshing paraslist ....%d, %s' % (id, str(self.model.showcontent)))
            panel = Panel_choose_pointlist_overwrite.Panel_Choose_Point(self._parent, self.pts_path, current_selection=id)
            self._parent.GetSizer().Add(panel, 0, 0, 5)
            self.controllist[0] = panel
            controlfile_tools.log_bystatus('Sending show content to other paras panel, %s' % str(self.model.showcontent))
            # pub.sendMessage('get_paras_main_data', data=(self.model.showcontent, ))

        elif check_list and 'condition' in check_list:
            import os
            self.if_conditiondata_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../condition_data.yml')
            panel = Panel_edit_if_condition_overwrite.Panel_edit_ifcondition(self._parent, self.if_conditiondata_path)
            self._parent.GetSizer().Add(panel, 0, 0, 5)
            self.controllist[0] = panel
            pub.sendMessage('get_if_condition_paras', data=(self.model.showcontent))

        else:
            for key in check_list:
                panel = Panel_edit_paras_overwrite.panel_edit_paras(self._parent, control=self, key=key,
                                                                    value=self.model.showcontent[key])
                self._parent.GetSizer().Add(panel, 0, 0, 5)
                self.controllist[key] = panel

    def _remove_allcontrols(self):
        sizer = self._parent.GetSizer()
        for i in range(len(sizer.GetChildren())):
            sizer.Hide(0)
            sizer.Remove(0)


    def _get_MainMsg(self, data):
        """get pts path from publiser"""
        controlfile_tools.log_bystatus('get Msg from Main, %s' % str(data), 'i')
        (self.pts_path, ) = data
        # pub.sendMessage('refresh_choosedatalist', data=(datalist, ))

    def get_errormsg(self):
        return self.check_value_msg[self.function_name]

    def set_functionname(self, func_name):
        self.function_name = func_name

    def check_functionlimits(self, func_name, value):
            controlfile_tools.log_bystatus('Checking function limit result is %s' % str(self.check_value[func_name](value)))
            return self.check_value[func_name](value)

### condition to check whether the value of default parameters panel is available.
    def check_speed_or_accel_value(self, value):
        return 0.0 < value < 100.0

    def check_io_value(self, value):
        return value in range(1)

    def check_naturalnumber_value(self, value):
        return  value > 0
#! encoding: utf-8
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

    def __init__(self, parent, pts_path = None):
        self._parent = parent
        self.pts_path = pts_path
        self.model = parameters_object.container()
        self.controllist = {}
        self.if_conditiondata_path = None
        pub.subscribe(self.refresh_paras_panel1, 'refresh_paras')
        pub.subscribe(self._remove_allcontrols, 'remove_all_paras')
        pub.subscribe(self._get_MainMsg, 'get_main_msg')

    #
    # def unselete_process_all(self):
    #     pub.sendMessage('unselete_process_all', data = ())

    def save_content_from_gui(self, text_content, _type):
        controlfile_tools.log_bystatus('text_content is %s, type is %s' % (text_content, _type), 'i')
        save_data = command_tools.check_type(text_content, _type)
        controlfile_tools.log_bystatus('save_data is %s' % save_data, 'i')
        if save_data != None:
            self.request_save_data()
            controlfile_tools.log_bystatus('request saving data %s' % save_data, 'i')
        else:
            return False
        return True

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
        self.model.model = data
        self.model.pos = pos
        return self.model.get_paras()

    def set_bitmap(self, btn_obj, bitmap_style = 'ok'):
        if bitmap_style == 'ok':
            btn_obj.SetBitmap(wx.ArtProvider.GetBitmap(u"gtk-ok", wx.ART_BUTTON))
        else:
            btn_obj.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_LIST_VIEW, wx.ART_BUTTON))

    def refresh_paras_panel1(self, data, pos):
        # TODO: Implement refresh_paras_panel
        # show_content = self.control.load_show_content( data, pos )
        controlfile_tools.log_bystatus('Entering refresh_paras_panel1... %s' % str(data) )
        self.controllist.clear()
        self._remove_allcontrols()
        ##-----------------------init value------------------
        reorder_list = [list('XYZUVW'), 'J1,J2,J3,J4,J5,J6'.split(',')]
        self.model.showcontent = data
        print 'data is ', self.model.showcontent, '.......'
        sizer = self._parent.GetSizer()
        #-------------------Logic-----------------
        if data:
            check_list = self.model.showcontent.keys()
            for check in reorder_list:
                if check_list[0] in check:
                    check_list = check
                    break
                else:
                    continue
            controlfile_tools.log_bystatus('keys is .....%s' % str(check_list), 'i')

            self._refresh_paraslist(check_list)

            controlfile_tools.log_bystatus("Find %d controls to layout, data str is %s"
                                           % (len(data), data), 'i')

        else:
            controlfile_tools.log_bystatus("Don't have any control to refresh!", 'e')
        sizer.Layout()

    def _refresh_paraslist(self, check_list):
        controlfile_tools.log_bystatus('check_list is %s ' % str(check_list))

        if len(check_list) == 1 and check_list[0] == 'choose_point':
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
            self.if_conditiondata_path = 'control/if_condition_data.yml'
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
        controlfile_tools.log_bystatus('get Msg from Main, %s' % str(data), 'i')
        (self.pts_path, ) = data
        # pub.sendMessage('refresh_choosedatalist', data=(datalist, ))

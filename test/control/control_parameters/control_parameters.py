#! encoding: utf-8
import copy
import wx
from test.data.object_parameters import parameters_object
from test.control.tools import command_tools
from test.control.tools import controlfile_tools
from test.view.view_parameters import Panel_edit_paras_overwrite


try:
    from wx.lib.pubsub import pub
except ImportError:
    from pubsub import pub


class Control():

    def __init__(self, parent):
        self._parent = parent
        self.model = parameters_object.container()
        self.controllist = {}
        pub.subscribe(self.refresh_paras_panel1, 'refresh_paras')
        pub.subscribe(self._remove_allcontrols, 'remove_all_paras')

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
        print 'self.controllist ', self.controllist
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
        self.controllist.clear()
        self.model.showcontent = data
        print 'data is ', self.model.showcontent, '.......'
        sizer = self._parent.GetSizer()
        self._remove_allcontrols()
        if data:
            for key, values in self.model.showcontent.iteritems():
                panel = Panel_edit_paras_overwrite.panel_edit_paras(self._parent, control=self, key=key, value=values)
                sizer.Add(panel, 0, 0, 5)
                self.controllist[key] = panel
            controlfile_tools.log_bystatus("Find %d controls to layout, data str is %s"
                                           % (len(data), data), 'i')

        else:
            controlfile_tools.log_bystatus("Don't have any control to refresh!", 'e')
        sizer.Layout()

    def _remove_allcontrols(self):
        sizer = self._parent.GetSizer()
        for i in range(len(sizer.GetChildren())):
            sizer.Hide(0)
            sizer.Remove(0)

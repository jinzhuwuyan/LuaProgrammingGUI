#！encoding: utf-8
"""Subclass of If_Condition_Panel, which is generated by wxFormBuilder."""
import os
import wx
import yaml
import GUI_IF_Codition
import logging
from LuaProgrammingGUI.test.control.control_parameters.control_if_condition import IFConditionControl
from LuaProgrammingGUI.test.control.tools import controlfile_tools
# Implementing If_Condition_Panel
class Panel_edit_ifcondition( GUI_IF_Codition.If_Condition_Panel ):

        def __init__(self, parent):

            self.ifcontrol = IFConditionControl(self, 'LuaProgrammingGUI/test/control/if_condition_data.yml')
            self.log = logging
            GUI_IF_Codition.If_Condition_Panel.__init__( self, parent )
            self.parent = parent
            self.condition_data_path = 'LuaProgrammingGUI/test/control/if_condition_data.yml'
            self.control_condition_data = None
            self.conditions = [u'判断输入IO', u'判断输出IO', u'判断位置']
            self.operations = {u'判断输入IO': [u'已开启', u'未开启'], u'判断输出IO': [u'已开启1', u'未开启1'], u'判断位置': [u'已到达', u'未到达'] }
            self.values = {u'判断输入IO': [unicode(in_io) for in_io in range(64)],
                           u'判断输出IO': [unicode(out_io) for out_io in range(32)],
                           u'判断位置': [unicode('P%d' % pos) for pos in range(100)]}

            # # 初始化条件控制语句列表控件
            # self.ifcontrol.tree = self.showconditiontree
            self.ifcontrol.parse_condition_data()
            # self.init_ifcondition_paneldata()
            self.refresh_choiceboxs(0, 9, 0)
            self.ifcontrol.model.items = [(u'判断输入IO', [], {'condition_value': u'9', 'operation_value': u'已开启'}),
                                          (u'判断输出IO', [], {'condition_value': u'11', 'operation_value': u'未开启1'}),
                                          (u'判断位置', [], {'condition_value': u'P9', 'operation_value': u'已到达'}),
                                          ]
            self.showconditiontree.RefreshItems()
            self.showconditiontree.Bind(wx.EVT_TREE_SEL_CHANGED, self.change_tree_selection)



        # Handlers for If_Condition_Panel events.
        def set_choose_mode( self, event ):
            # TODO: Implement set_choose_mode
            self.ifcontrol.set_choose_mode(event.EventObject)

        def add_condition( self, event ):
            # TODO: Implement add_condition
            self.ifcontrol.add_condition(event.EventObject)

        def delete_condition( self, event ):
            # TODO: Implement delete_condition
            self.ifcontrol.delete_conditon(event.EventObject)

        def choose_condition( self, event ):
            # TODO: Implement choose_condition
            self.ifcontrol.choose_condition(event.EventObject)
            self.refresh_choiceboxs(event.EventObject.GetSelection(), 0, 0)

            selection_info = self.ifcontrol.get_tree_item_info(self.showconditiontree)
            if selection_info:
                select_id, condition_str, condition_value = selection_info
                new_item_str = self.m_choice_choosecondition.GetStringSelection()
                _tmp_value = {}
                _tmp_value['condition_value'] = self.values[new_item_str][0]
                _tmp_value['operation_value'] = self.operations[new_item_str][0]

                newitem = (new_item_str, [], _tmp_value)
                self.ifcontrol.model.items[select_id] = newitem
                self.showconditiontree.RefreshItems()
            else:
                pass


        def choose_operation( self, event ):
            # TODO: Implement choose_operation
            self.ifcontrol.choose_operation(event.EventObject)
            selection_info = self.ifcontrol.get_tree_item_info(self.showconditiontree)
            if selection_info:
                select_id, condition_str, condition_value = selection_info
                _, _, select_value = self.ifcontrol.model.items[select_id]
                select_value['operation_value'] = unicode(self.m_choice_choosecontrol.GetStringSelection())
                self.showconditiontree.RefreshItems()
            else:
                pass


        def choose_value( self, event ):
            # TODO: Implement choose_value
            self.ifcontrol.choose_value(event.EventObject)
            selection_info = self.ifcontrol.get_tree_item_info(self.showconditiontree)
            if selection_info:
                select_id, condition_str, condition_value = selection_info
                _, _, select_value = self.ifcontrol.model.items[select_id]
                select_value['condition_value'] = unicode(self.m_choice_choosevalue.GetStringSelection())
                controlfile_tools.log_bystatus('select_value is %s' % str(select_value))
                self.showconditiontree.RefreshItems()
            else:
                pass

        def change_tree_selection(self, event):
            selection_info = self.ifcontrol.get_tree_item_info(event.EventObject)
            if selection_info:

                    select_id, condition_str, condition_value = selection_info
                    operation_list = self.operations[condition_str]
                    controlfile_tools.log_bystatus('operation_id is %s, value_id is %s' % (str(operation_list), condition_value['operation_value']))
                    operation_id = self.ifcontrol.get_condition_id(operation_list, condition_value['operation_value'])
                    value_list = self.values[condition_str]
                    value_id = self.ifcontrol.get_condition_id(value_list, condition_value['condition_value'])
                    controlfile_tools.log_bystatus('operation_id is %d, value_id is %d' % (operation_id, value_id))
                    if operation_id != -1 and value_id != -1:

                        self.refresh_choiceboxs(select_id, value_id, operation_id)
                    else:
                        pass
            else:
                pass

        def init_ifcondition_paneldata(self):
            try:
                with open(os.path.abspath(self.condition_data_path)) as f:
                    self.control_condition_data = yaml.load(f.read())
                    self.parse_condition_data()
                    # self.refresh_choiceboxs()
            except Exception as e:
                print e
                wx.MessageBox('初始化界面失败！请询问技术人员具体原因！')

        def parse_condition_data(self):
            del self.conditions[:]
            del self.operations[:]
            if self.control_condition_data:
                condition = self.control_condition_data[-1]
                (condition_str, value) = condition

                for v in self.parse_value(value):
                    self.values.append(v)
                for c in self.control_condition_data:
                    (condition_str, _) = condition
                    self.conditions.append(condition_str)
                # self.parent.refresh_choiceboxs()
            else:
                pass

        def parse_value(self, value):
            if isinstance(value, list):
                self.operations = [u'等于', u'不等于']
                return [str(v) for v in value]
            elif isinstance(value, dict):
                if 'Point' in value.keys():
                    for points in value['Point']:
                        self.operations.append(u'等于%d' % points)
                    return ['P%d' % d for d in xrange(100)]
            else:
                return ['0', '1']

        def refresh_choiceboxs(self, condition_index, value_index, control_index):
            # print 'self.ifcontrol.conditions is %s' % str(self.ifcontrol.conditions)
            # print 'self.ifcontrol.operations is %s' % str(self.ifcontrol.operations)
            # print 'self.ifcontrol.values is %s' % str(self.ifcontrol.values)
            self.m_choice_choosecondition.SetItems(self.conditions)
            self.m_choice_choosecondition.SetSelection(condition_index)
            self.m_choice_choosecontrol.SetItems(self.operations[unicode(self.m_choice_choosecondition.GetStringSelection())])
            self.m_choice_choosevalue.SetItems(self.values[unicode(self.m_choice_choosecondition.GetStringSelection())])
            self.m_choice_choosecondition.Refresh()
            self.m_choice_choosecontrol.Refresh()
            self.m_choice_choosevalue.Refresh()
            self.m_choice_choosecontrol.SetSelection(control_index)
            self.m_choice_choosevalue.SetSelection(value_index)

if __name__ == '__main__':
    app = wx.App()
    Panel_edit_ifcondition(None).Show(True)
    app.MainLoop()
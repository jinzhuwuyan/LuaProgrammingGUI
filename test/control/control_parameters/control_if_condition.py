#! encoding: utf-8
import wx
import os
import yaml
from LuaProgrammingGUI.test.control.tools import command_tools
from LuaProgrammingGUI.test.control.tools import controlfile_tools
from LuaProgrammingGUI.test.data.object_parameters import conditiontree_object

try:
    from wx.lib.pubsub import pub
except ImportError:
    from pubsub import pub

class IFConditionControl():

    def __init__(self, parent, control_data_path):
        self.parent = parent
        self.default_item = (u'判断输入信号', [], {'condition_value': u'in(0)', 'operation_value': u'已开启'})
        self.control_condition_data = None
        self.model = None
        self.tree = None
        self.choice_conditions = None
        self.choice_controls = None
        self.choice_conditions = None
        self.radio_allcondition = None
        self.radio_onlyonecondition = None
        self.conditions = None
        self.operations = None
        self.values = None
        self.refresh_data = None
        self.check_allconditions = None
        self.condition_data_path = control_data_path
        self.config()

    def config(self):

        # 初始化if条件列表的数据模型
        self.model = conditiontree_object.Condition_Tree_Container()
        # 初始化刷新数据内容
        self.refresh_data = {'condition': (self.model.items, 'list'), 'check_allconditions': self.check_allconditions}
        # 初始化if条件参数控件的数据
        self.init_ifcondition_paneldata()
        # 初始化对应控制语句的参数数据
        pub.subscribe(self.refresh_paras, 'get_if_condition_paras')



    def refresh_paras(self, data):
        # 初始化条件控制语句列表控件

        controlfile_tools.log_bystatus('recv refresh if conditions paras data is %s' % str(data))
        self.model.items = data['condition'][0]
        self.check_allconditions = data['check_allconditions']
        self.radio_allcondition.SetValue(self.check_allconditions)
        self.radio_onlyonecondition.SetValue(not self.check_allconditions)
        controlfile_tools.log_bystatus('para[condition] is %s' % str(data['condition'][0]))
        controlfile_tools.log_bystatus('recv refresh self.model.items is %s' % str(self.model.items))
        controlfile_tools.log_bystatus('recv refresh self.check_allconditions is %s' % str(self.check_allconditions))

        self.refresh_tree()
        self.parent.Refresh()
        # self.parse_condition_data()
        # self.refresh_choiceboxs()

    def set_tree(self, tree):
        self.tree = tree

        self.choice_conditions = self.parent.m_choice_choosecondition
        self.choice_controls = self.parent.m_choice_choosecontrol
        self.choice_values = self.parent.m_choice_choosevalue
        self.radio_allcondition = self.parent.m_radioBtn_allneed
        self.radio_onlyonecondition = self.parent.m_radioBtn_onlyone

    def refresh_tree(self):
        self.tree.RefreshItems()

    def unselect_tree(self):
        self.tree.UnselectAll()

    def set_choose_mode(self, obj):
        self.check_allconditions = self.radio_allcondition.GetValue()
        self.radio_allcondition.SetValue(self.check_allconditions)
        self.radio_onlyonecondition.SetValue(not self.check_allconditions)

        self.refresh_data['check_allconditions'] = self.check_allconditions

        self.refresh_data['condition'] = (self.model.items[:], 'list')
        controlfile_tools.log_bystatus("set_choose_mode's refresh_data is %s " % str(self.refresh_data))
        pub.sendMessage('save_paras', refresh_type='refresh', data=self.refresh_data)
        controlfile_tools.log_bystatus("set_choose_mode's refresh_data is %s " % str(self.refresh_data))



    def add_condition(self, obj):
        tree_selection_info = self.get_tree_item_info(self.tree)
        if tree_selection_info:
            select_id, condition_str, condition_value = tree_selection_info
            self.model.items.insert(select_id + 1, self.default_item)
        else:
            self.model.items.append(self.default_item)
        self.refresh_tree()
        self.unselect_tree()
        pub.sendMessage('save_paras', refresh_type='refresh', data=self.refresh_data)

    def delete_condition(self, obj):

        tree_selection_info = self.get_tree_item_info(self.tree)
        if tree_selection_info:
            select_id, condition_str, condition_value = tree_selection_info
            self.model.items.pop(select_id)
            self.choice_conditions.Clear()
            self.choice_controls.Clear()
            self.choice_values.Clear()
            self.refresh_tree()
            self.unselect_tree()
            pub.sendMessage('save_paras', refresh_type='refresh', data=self.refresh_data)
        else:
            wx.MessageBox(u'请选中一个条件进行删除！')


    def choose_condition(self, obj):

        pass

    def choose_operation(self, obj):

        pass

    def choose_value(self, obj):

        pass

    def get_tree_item_info(self, obj):
        select_item = obj.GetSelection()
        selection = obj.GetIndexOfItem(select_item)
        if len(selection) > 0:
            (select_id,) = selection
            condition_str, _, condition_value = self.model.items[select_id]
            return select_id, condition_str, condition_value
        else:
            return None

    def get_condition_id(self, condition_list, condition_value):
        for idx, value in enumerate(condition_list):
            if unicode(value) == unicode(condition_value):
                return idx
            else:
                continue
        return -1

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
        self.conditions = self.control_condition_data['condition']
        self.values = self.control_condition_data['value']
        self.operations = self.control_condition_data['operation']
        controlfile_tools.log_bystatus('condition is %s, value is %s, operation is %s '
                                       % (str(self.conditions), str(self.values), str(self.operations)) )

    def init_choiceboxs(self, condition_idx):
        # 条件列表刷新初始化
        self.choice_conditions.SetItems(self.conditions)
        self.choice_conditions.Refresh()
        self.choice_conditions.SetSelection(condition_idx)
        condition_selection_str = self.choice_conditions.GetStringSelection()

        # 控制列表刷新初始化
        self.choice_controls.SetItems(self.operations[unicode(condition_selection_str)])
        self.choice_controls.Refresh()
        # 条件值列表初始化
        self.choice_values.SetItems(self.values[unicode(condition_selection_str)])
        self.choice_values.Refresh()

    def refresh_choiceboxs(self, condition_index, value_index, control_index):
        self.init_choiceboxs(condition_index)
        self.choice_conditions.SetSelection(condition_index)
        self.choice_controls.SetSelection(control_index)
        self.choice_values.SetSelection(value_index)
        print 'condition index is %d, value index is %d, control index is %d' % (condition_index, value_index, condition_index)


    def change_tree_selection(self, obj):
        selection_info = self.get_tree_item_info(obj)
        if selection_info:

            select_id, condition_str, condition_value = selection_info
            condition_id = self.get_condition_id(self.conditions, condition_str)
            operation_list = self.operations[condition_str]
            controlfile_tools.log_bystatus(
                'select_id is %s, operation_id is %s, value_id is %s' % (str(select_id), str(operation_list), condition_value['operation_value']))
            operation_id = self.get_condition_id(operation_list, condition_value['operation_value'])
            value_list = self.values[condition_str]
            value_id = self.get_condition_id(value_list, condition_value['condition_value'])
            controlfile_tools.log_bystatus('operation_id is %d, value_id is %d' % (operation_id, value_id))
            if operation_id != -1 and value_id != -1:

                self.refresh_choiceboxs(condition_id, value_id, operation_id)
            else:
                self.init_choiceboxs(condition_id)
        else:
            pass
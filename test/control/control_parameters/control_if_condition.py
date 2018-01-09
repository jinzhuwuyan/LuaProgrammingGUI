#! encoding: utf-8
import wx
import os
import yaml
from control.tools import command_tools
from control.tools import controlfile_tools
from data.object_parameters import conditiontree_object

try:
    from wx.lib.pubsub import pub
except ImportError:
    from pubsub import pub

class IFConditionControl():
    """
                .. admonition:: Class Infos

                        |  *class_description*:
                        |        Maintain the if condition panel paras
                        |
                        |  *class_chinese_description*:
                        |        初始化if条件树(:meth:`refresh_paras`)
                        |        if条件树的数据维护控制(:meth:`add_condition`, :meth:`delete_condition`, :meth:`change_tree_selection`)
                        |        刷新条件树参数(:meth:`save_paras`)
                        |
                        |
                        |
                        | The **initilization** of :class:`IFConditionControl` is:
                        |        control = (view_instance, control_data_path)
                        |
                        |
                        | **Parameters of initilization**:
                        |
                        |       **view_instance** : :class:`~view.view_parameters.Panel_edit_if_condition_overwrite.Panel_edit_ifcondition`  or its subclass
                        |
                        |       **control_data_path** : str
                        |               the exist path of initilizing the condition panel's data
                        |
                        |
                        |
                        |

    """
    def __init__(self, parent, control_data_path):
        self.parent = parent
        # 默认添加的item
        self.default_item = None
        # 控制if条件面板数据，配置文件容器
        self.control_condition_data = None
        # 数据模型
        self.model = None
        # 显示条件树
        self.tree = None
        # 条件列表控件
        self.choice_conditions = None
        # 操作值列表控件
        self.choice_controls = None
        # 条件值列表控件
        self.choice_values = None
        # 选择全部满足控件
        self.radio_allcondition = None
        # 选择只满足一个条件控件
        self.radio_onlyonecondition = None
        # 条件控件数据
        self.conditions = None
        # 操作控件数据
        self.operations = None
        # 值控件数据
        self.values = None
        # 请求刷新ifcondition数据的内容
        self.refresh_data = None
        # 检查是否选择了全部满足的变量
        self.check_allconditions = None
        # 操作值所对应的实际内容值
        self.operation_values = None
        # if 条件数据地址
        self.condition_data_path = control_data_path
        self.config()

    def config(self):
        """config the control"""
        # 初始化if条件列表的数据模型
        self.model = conditiontree_object.Condition_Tree_Container()
        # 初始化if条件参数控件的数据
        self.init_ifcondition_paneldata()
        # 初始化对应控制语句的参数数据
        pub.subscribe(self.refresh_paras, 'get_if_condition_paras')

    def refresh_paras(self, data):
        """
        reinit the paras controls with the condition data
        :param `data`: the condition data for initilization
        :type `data`: dict
        """
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

    def set_tree(self, tree):
        """set if condition tree and init other controls of parent"""
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
        """
        set all conditions satisfy or only one condition satisfy
        :param `obj`: event Object
        :type `obj`: wx.Event
        """
        self.check_allconditions = self.radio_allcondition.GetValue()
        self.radio_allcondition.SetValue(self.check_allconditions)
        self.radio_onlyonecondition.SetValue(not self.check_allconditions)

        self.refresh_data['check_allconditions'] = self.check_allconditions

        self.refresh_data['condition'] = (self.model.items[:], 'list')
        controlfile_tools.log_bystatus("set_choose_mode's refresh_data is %s " % str(self.refresh_data))
        self.save_paras()



    def add_condition(self, obj):
        """add one condiiton"""
        __default_item = (u'判断输入信号', [], {'condition_value': u'getInput(0)', 'operation_value': u'有信号'})
        tree_selection_info = self.get_tree_item_info(self.tree)
        if tree_selection_info:
            select_id, condition_str, condition_value = tree_selection_info
            self.model.items.insert(select_id + 1, __default_item)
        else:
            self.model.items.append(__default_item)
        self.refresh_tree()
        self.unselect_tree()
        self.save_paras()

    def delete_condition(self, obj):
        """delete selected condition"""
        tree_selection_info = self.get_tree_item_info(self.tree)
        if tree_selection_info:
            select_id, condition_str, condition_value = tree_selection_info
            self.model.items.pop(select_id)
            self.choice_conditions.Clear()
            self.choice_controls.Clear()
            self.choice_values.Clear()
            self.refresh_tree()
            self.unselect_tree()
            self.save_paras()
        else:
            wx.MessageBox(u'请选中一个条件进行删除！')


    def save_paras(self):
        """save condition paras to control process panel"""
        self.refresh_data['condition'] = (self.model.items[:], 'list')
        pub.sendMessage('save_paras', refresh_type='refresh', data=self.refresh_data)

    def choose_condition(self, obj):
        """
        choose condition control to set condition value and refresh other operation and value controls
        :param `obj`: condition control
        :type `obj`: wx.Choice
        """
        self.refresh_choiceboxs(obj.GetSelection(), 0, 0)

        selection_info = self.get_tree_item_info(self.tree)
        if selection_info:
            select_id, condition_str, condition_value = selection_info
            new_item_str = self.choice_conditions.GetStringSelection()
            _tmp_value = {}
            _tmp_value['condition_value'] = self.values[new_item_str][0]
            _tmp_value['operation_value'] = self.operations[new_item_str][0]

            newitem = (new_item_str, [], _tmp_value)
            self.model.items[select_id] = newitem
            self.tree.RefreshItems()
            self.save_paras()
        else:
            pass

    def choose_operation(self, obj):
        """choose operation value"""
        selection_info = self.get_tree_item_info(self.tree)
        if selection_info:
            select_id, condition_str, condition_value = selection_info
            _, _, select_value = self.model.items[select_id]
            select_value['operation_value'] = unicode(self.choice_controls.GetStringSelection())
            self.tree.RefreshItems()
            self.save_paras()
        else:
            pass

    def choose_value(self, obj):
        """choose value"""
        selection_info = self.get_tree_item_info(self.tree)
        if selection_info:
            select_id, condition_str, condition_value = selection_info
            _, _, select_value = self.model.items[select_id]
            select_value['condition_value'] = unicode(self.choice_values.GetStringSelection())
            controlfile_tools.log_bystatus('select_value is %s' % str(select_value))
            self.tree.RefreshItems()
            self.save_paras()
        else:
            pass

    def get_tree_item_info(self, obj):
        """
        get condition infos by condition tree selection
        :param `obj`:  condition tree
        :type `obj`: wx.TreeListCtrl
        :return: (selection id, condition string, condition value)
        :rtype: tuple
        :exception:
            there are no selection, then return None

        """
        select_item = obj.GetSelection()
        selection = obj.GetIndexOfItem(select_item)
        if len(selection) > 0:
            (select_id,) = selection
            condition_str, _, condition_value = self.model.items[select_id]
            return select_id, condition_str, condition_value
        else:
            return None

    def get_condition_id(self, condition_list, condition_value):
        """
        get condition position with condition list
        :param `condition_list`: condition list
        :type `condition_list`: list
        :param `condition_value`: checkvalue
        :type `condition_value`: str
        :return: position id
        :exception:
            if condition list don't have check value, then return -1
        """
        for idx, value in enumerate(condition_list):
            if unicode(value) == unicode(condition_value):
                return idx
            else:
                continue
        return -1

    def init_ifcondition_paneldata(self):
        """init condition panel data"""
        try:
            with open(os.path.abspath(self.condition_data_path)) as f:
                self.control_condition_data = yaml.load(f.read())
                self.parse_condition_data()

                # self.refresh_choiceboxs()
        except Exception as e:
            print e
            wx.MessageBox('初始化界面失败！请询问技术人员具体原因！')

    def parse_condition_data(self):
        """parse condition data to variable"""
        self.conditions = self.control_condition_data['condition']
        self.values = self.control_condition_data['value']
        self.operations = self.control_condition_data['operation']
        self.default_item = self.control_condition_data['default_append_item']
        self.refresh_data = self.control_condition_data['default_refresh_data']
        self.operation_values = self.control_condition_data['operation_values']
        controlfile_tools.log_bystatus('condition is %s, value is %s, operation is %s '
                                       % (str(self.conditions), str(self.values), str(self.operations)) )

    def init_choiceboxs(self, condition_idx):
        """init choices controls with condition value chosen"""
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
        """set condition, value, control selection with indexs"""
        self.init_choiceboxs(condition_index)
        self.choice_conditions.SetSelection(condition_index)
        self.choice_controls.SetSelection(control_index)
        self.choice_values.SetSelection(value_index)
        print 'condition index is %d, value index is %d, control index is %d' % (condition_index, value_index, condition_index)


    def change_tree_selection(self, obj):
        """change condition tree condition and change the choices selection"""
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
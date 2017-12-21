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
        self.control_condition_data = None
        self.model = None
        self.tree = None
        self.conditions = None
        self.operations = None
        self.values = None
        self.condition_data_path = control_data_path
        self.config()

    def config(self):

        self.conditions = []
        self.operations = []
        self.values = []

        # 初始化if条件列表的数据模型
        self.model = conditiontree_object.Condition_Tree_Container()
        # 初始化if条件参数控件的数据
        # self.init_ifcondition_paneldata()
        # 初始化对应控制语句的参数数据
        pub.subscribe(self.refresh_paras, 'refresh_paras')
        # 解析发送过来的数据并刷新内容




    def init_ifcondition_paneldata(self):
        try:
                controlfile_tools.log_bystatus('condition data path is %s ' % str(os.path.abspath(self.condition_data_path)))
                with open(self.condition_data_path) as f:
                    self.control_condition_data = yaml.load(f.read())
                    self.parse_condition_data()

        except Exception as e:
            print e
            wx.MessageBox('初始化界面失败！请询问技术人员具体原因！')


    def refresh_paras(self, data, pos):
        # 初始化条件控制语句列表控件
        self.tree = self.parent.showconditiontree
        controlfile_tools.log_bystatus('recv refresh if conditions paras data is %s' % str(data))
        # self.model.items = data['condition'][0]

        controlfile_tools.log_bystatus('para[condition] is %s' % str(data['condition'][0]))
        self.model.items = []
        self.refresh_tree()
        # self.parse_condition_data()
        # self.refresh_choiceboxs()

    def parse_condition_data(self):
        controlfile_tools.log_bystatus('parse condition data is %s' % str(self.control_condition_data))
        del self.conditions[:]
        del self.values[:]
        del self.operations[:]
        if self.control_condition_data:
                condition = self.control_condition_data[-1]
                (condition_str, value) =  condition

                controlfile_tools.log_bystatus('parse value is %s' % str(value))
                for v in self.parse_value(value):
                    self.values.append(v)
                for c in self.control_condition_data:
                    (condition_str, _) = condition
                    self.conditions.append(condition_str)
                self.parent.refresh_choiceboxs()
        else:
            pass
        controlfile_tools.log_bystatus('parse again condition data is %s' % str(self.control_condition_data))



    def parse_value(self, value):
        if isinstance(value, list):
            self.operations = [u'等于', u'不等于']
            return [str(v) for v in value]
        elif isinstance(value, dict):
            if 'Point' in value.keys():
                for points in  value['Point']:
                    self.operations.append(u'等于%d' % points)
                return ['P%d' % d for d in xrange(100)]
        else:
            return ['0', '1']

    def refresh_tree(self):
        self.tree.RefreshItems()

    def unselect_tree(self):
        self.tree.UnselectAll()

    def set_choose_mode(self, obj):
        pass


    def add_condition(self, obj):

        pass

    def delete_condition(self, obj):

        pass

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

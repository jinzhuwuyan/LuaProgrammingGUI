#! encoding: utf-8
import wx
from LuaProgrammingGUI.test.control.tools import command_tools
from LuaProgrammingGUI.test.control.tools import controlfile_tools
from LuaProgrammingGUI.test.data.object_parameters import conditiontree_object

try:
    from wx.lib.pubsub import pub
except ImportError:
    from pubsub import pub

class IFConditionControl():

    def __init__(self, parent):
        self.model = conditiontree_object.Condition_Tree_Container()


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

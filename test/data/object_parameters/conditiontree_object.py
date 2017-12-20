from LuaProgrammingGUI.test.view.view_process import TreeMixin
class Condition_Tree_Container(TreeMixin.TreeModel):

    def __init__(self, *args, **kwargs):
        TreeMixin.TreeModel.__init__(self, *args, **kwargs)
        self.modeldata = []


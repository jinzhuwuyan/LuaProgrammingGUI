from test.view.view_process import TreeMixin
class container(TreeMixin.TreeModel):

    def __init__(self, *args, **kwargs):
        TreeMixin.TreeModel.__init__(self, *args, **kwargs)
        self.modeldata = []


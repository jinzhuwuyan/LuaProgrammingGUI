from test.view.control_process import TreeMixin
class container():

    def __init__(self):
        self.change_status = False
        # [self.id, self.parentid, self.childid] = [0] * 3
        self.model = TreeMixin.TreeModel()



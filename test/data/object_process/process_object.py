from test.view.control_process import TreeMixin
from test.data.function_list import function_object
class container():

    def __init__(self):
        self.change_status = False
        # [self.id, self.parentid, self.childid] = [0] * 3
        self.model = TreeMixin.TreeModel()

    # def append(self, data, pos):
    #     self.mod

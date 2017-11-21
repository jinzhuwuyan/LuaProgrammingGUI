import copy
class container():

    def __init__(self):

        # self.model = {}
        # self.pos = []
        self.model  = {'1': {'2': {'3': {'5': {'test': {'X': '1', 'Y': 'ss'}}}, '4': {}}}}
        self.pos = ['1', '2', '3', '5', 'test']
        self._tmppos = []

    def  get_paras(self):
        # _tmp = copy.deepcopy(self.model)
        # for pos in self.pos:
        #     _tmp = _tmp[pos]
        # return _tmp
        return self.model

    def set_paras(self, text_content):
        self._tmppos = copy.deepcopy(self.pos)
        self._tmppos.reverse()
        _tmp = self.model
        for pos in self.pos:
            _tmp = _tmp[pos]
        _tmp = text_content
        print self.model
        print _tmp





if __name__ == '__main__':
    c = container()
    c.model = {'1': {'2': {'3': {'5': {'test': 'xxxx'}}, '4': {}}}}
    c.pos = ['1', '2', '3', '5', 'test']
    print c.get_paras()
    c.set_paras('sza')
    # print c.model


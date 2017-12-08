import wx
from pureSpinCtrl import FloatSpin

class FloatSpinCtrl(FloatSpin):
    def __init__(self, parent, id, style, pos, sizer, value, min_val, max_val, inital):

        FloatSpin.__init__(self, parent, id, pos=pos, size=sizer, min_val=0, max_val=1,
                                 increment=0.01, value=0.0, digits=3)



#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
**Module Info**::

   @Author     : yan_sw
   @Time       : 2018-01-10 08:57
   @Description:
        Common handler which other demos must realize

"""

try:
    from wx.lib.pubsub import pub
except ImportError:
    from pubsub import pub

class CommandHander(object):

    def __init__(self):
        pub.subscribe(self.__handler, 'update_demos')

    def __handler(self, data):
        """Don't change!"""
        self.return_luaprogrammingpanel(self.generate_demos(data=data))

    def generate_demos(self, data):
        pass


    def return_luaprogrammingpanel(self, data):
        pass

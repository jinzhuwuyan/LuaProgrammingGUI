
try:
    from wx.lib.pubsub import pub
except ImportError:
    from pubsub import pub

from threading import Thread
from test.control.tools import controlfile_tools

def config_control(self, id, pos, size, style):

    self.SetId(id)
    self.SetPosition(pos)
    self.SetSize(size)
    self.SetWindowStyle(style)

class AsyncMessageHandler(Thread):

    def __init__(self, *args, **kwargs):
        super(Thread, self).__init__(*args, **kwargs)
        self.daemon = True
        self.parent = kwargs.pop('parent')
        self.from_which = None
        self.to_which = None
        self._current_data = []
        self.eventqueue = []
        self.eventhistory = []
        pub.subscribe(self.Receive, "Handle")


    def run(self):
        while True:
            if self.eventqueue:
                event = self.eventqueue.reverse().pop()
                (data, self.from_which, self.to_which) = event
                if len(data) == 1:
                    (command) = data
                    if command == 'Save':
                        #save data to text
                        file_path, memorydata = self.get_currentdata()
                        self.create_thread(target=controlfile_tools.save, args=(file_path, memorydata))
                    elif command == 'Undo':
                        pass
                    else:
                        print command
                elif len(data) == 2:

                    if command == 'Append':
                        pass
                    elif command == 'Delete':
                        pass
                    elif command == 'Change':
                        pass
                else:
                    print event
            else:
                # save content to swp
                pass

    def Response(self, ret_obj):
        pub.sendMessage(self.to_which, ret_obj)

    def Receive(self, data, from_which_subscribe, to_which_subscribe = None):
        event = (data, from_which_subscribe, to_which_subscribe)
        self.eventqueue.append(event)

    def create_thread(self, target = None, args = None, kwargs = None):
        t = Thread(target=target, args=args, )
        t.daemon = False
        t.start()

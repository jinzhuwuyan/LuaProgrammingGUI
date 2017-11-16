from tools import controlfile_tools

# def check_none(func):
#     def wrapper(*args, **kwargs):
#         (self, event) = args
#         if self.parent == None:
#             deractor_controlfile.log_bystatus('Please init the parent with the type of %s'
#                                               % "<class 'Panel_controlprocess_overwrite.panel_process'>", 'e')
#         else:
#             return func(*args, **kwargs)
#     return wrapper


class Control():

    def __init__(self, parent):
        self.parent = parent

    def monitor_changes(self, event, status):
        event.Enable(status)







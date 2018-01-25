from control.tools import view_tools
import Panel_luaprogramming
class LuaProgrammingPanel(Panel_luaprogramming.Panel_luaprogramming):
    def __init__(self, parent, id, pos, size, style):
        Panel_luaprogramming.Panel_luaprogramming.__init__(self, parent)
        view_tools.config_control(self, id, pos, size, style)
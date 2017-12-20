# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Aug  3 2017)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

from wxPanel_overwrite import Panel
import wx
import wx.xrc
from TreeMixin import VirtualTreeCtrl
from TreeMixin import VirtualTreeListCtrl

###########################################################################
## Class Panel_controlprocess
###########################################################################

class Panel_controlprocess ( Panel ):
	
	def __init__( self, parent ):
		Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.TAB_TRAVERSAL )
		
		topsizer = wx.FlexGridSizer( 2, 0, 0, 0 )
		topsizer.AddGrowableCol( 0 )
		topsizer.AddGrowableRow( 1 )
		topsizer.SetFlexibleDirection( wx.BOTH )
		topsizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_toolBar_main = wx.ToolBar( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL ) 
		self.m_tool_add = self.m_toolBar_main.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_ADD_BOOKMARK, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, u"添加函数", u"添加函数", None ) 
		
		self.m_tool_delete = self.m_toolBar_main.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( u"gtk-cancel", wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, u"删除函数", u"删除函数", None ) 
		
		self.m_tool_up = self.m_toolBar_main.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_GO_UP, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, u"向上一级移动", u"向上一级移动", None ) 
		
		self.m_tool_down = self.m_toolBar_main.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_GO_DOWN, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, u"向下一级移动", u"向下一级移动", None ) 
		
		self.m_toolBar_main.AddSeparator()
		
		self.m_tool_save = self.m_toolBar_main.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( u"gtk-yes", wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, u"保存", u"保存", None ) 
		
		self.m_tool_redo = self.m_toolBar_main.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( u"gtk-undo", wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, u"恢复上次工作", u"恢复上次工作", None ) 
		
		self.m_tool_modify_run_time = self.m_toolBar_main.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( u"gtk-refresh", wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, u"修改循环时间", u"修改循环时间", None ) 
		
		self.m_toolBar_main.AddSeparator()
		
		self.m_tool_open_project = self.m_toolBar_main.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_FILE_OPEN, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, u"打开工程", u"打开工程", None ) 
		
		self.m_tool_save_to_otherpath = self.m_toolBar_main.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_FILE_SAVE_AS, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, u"另存为", u"另存为", None ) 
		
		self.m_toolBar_main.AddSeparator()
		
		self.m_tool_help = self.m_toolBar_main.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_HELP, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, u"帮助", u"帮助", None ) 
		
		self.m_toolBar_main.Realize() 
		
		topsizer.Add( self.m_toolBar_main, 0, wx.EXPAND, 5 )
		
		sizer_controldata = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_treeControl_show = VirtualTreeCtrl(self, treemodel=self.control.model, log=self.log)
		sizer_controldata.Add( self.m_treeControl_show, 1, wx.EXPAND, 5 )
		
		self.m_treeControl_showdata = VirtualTreeListCtrl(self, treemodel=self.showdatacontrol.model, log=self.log)
		sizer_controldata.Add( self.m_treeControl_showdata, 1, wx.EXPAND, 5 )
		
		
		topsizer.Add( sizer_controldata, 0, wx.EXPAND, 5 )
		
		
		self.SetSizer( topsizer )
		self.Layout()
		topsizer.Fit( self )
		
		# Connect Events
		self.Bind( wx.EVT_TOOL, self.add_functions, id = self.m_tool_add.GetId() )
		self.Bind( wx.EVT_TOOL, self.delete_functions, id = self.m_tool_delete.GetId() )
		self.Bind( wx.EVT_TOOL, self.take_function_up, id = self.m_tool_up.GetId() )
		self.Bind( wx.EVT_TOOL, self.take_function_down, id = self.m_tool_down.GetId() )
		self.Bind( wx.EVT_TOOL, self.save_change, id = self.m_tool_save.GetId() )
		self.Bind( wx.EVT_UPDATE_UI, self.check_save_status, id = self.m_tool_save.GetId() )
		self.Bind( wx.EVT_TOOL, self.redo_edit, id = self.m_tool_redo.GetId() )
		self.Bind( wx.EVT_TOOL, self.modify_runtime, id = self.m_tool_modify_run_time.GetId() )
		self.Bind( wx.EVT_TOOL, self.import_prj_fromdisk, id = self.m_tool_open_project.GetId() )
		self.Bind( wx.EVT_TOOL, self.output_to_folder, id = self.m_tool_save_to_otherpath.GetId() )
		self.Bind( wx.EVT_TOOL, self.show_process_control_help, id = self.m_tool_help.GetId() )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def add_functions( self, event ):
		event.Skip()
	
	def delete_functions( self, event ):
		event.Skip()
	
	def take_function_up( self, event ):
		event.Skip()
	
	def take_function_down( self, event ):
		event.Skip()
	
	def save_change( self, event ):
		event.Skip()
	
	def check_save_status( self, event ):
		event.Skip()
	
	def redo_edit( self, event ):
		event.Skip()
	
	def modify_runtime( self, event ):
		event.Skip()
	
	def import_prj_fromdisk( self, event ):
		event.Skip()
	
	def output_to_folder( self, event ):
		event.Skip()
	
	def show_process_control_help( self, event ):
		event.Skip()
	


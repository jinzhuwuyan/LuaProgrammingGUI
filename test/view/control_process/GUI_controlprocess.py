# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Aug  3 2017)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class Frame_controlprocess
###########################################################################

class Frame_controlprocess ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"control_process", pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		topsizer = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel_controlprocess = Panel_controlprocess( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		topsizer.Add( self.m_panel_controlprocess, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( topsizer )
		self.Layout()
		self.m_statusBar = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

###########################################################################
## Class Panel_controlprocess
###########################################################################

class Panel_controlprocess ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL )
		
		topsizer = wx.FlexGridSizer( 2, 0, 0, 0 )
		topsizer.AddGrowableCol( 0 )
		topsizer.AddGrowableRow( 1 )
		topsizer.SetFlexibleDirection( wx.BOTH )
		topsizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_toolBar_main = wx.ToolBar( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL ) 
		self.m_tool_add = self.m_toolBar_main.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_ADD_BOOKMARK, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, u"添加函数", u"添加函数", None ) 
		
		self.m_tool_delete = self.m_toolBar_main.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( u"gtk-no", wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, u"删除函数", u"删除函数", None ) 
		
		self.m_tool_up = self.m_toolBar_main.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_GO_UP, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, u"向上一级移动", u"向上一级移动", None ) 
		
		self.m_tool_down = self.m_toolBar_main.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_GO_DOWN, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, u"向下一级移动", u"向下一级移动", None ) 
		
		self.m_toolBar_main.AddSeparator()
		
		self.m_tool_save = self.m_toolBar_main.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( u"gtk-yes", wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, u"保存", u"保存", None ) 
		
		self.m_tool_redo = self.m_toolBar_main.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( u"gtk-undo", wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, u"撤销", u"撤销", None ) 
		
		self.m_toolBar_main.Realize() 
		
		topsizer.Add( self.m_toolBar_main, 0, wx.EXPAND, 5 )
		
		self.m_textCtrl_showtext = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_RICH )
		topsizer.Add( self.m_textCtrl_showtext, 0, wx.EXPAND, 5 )
		
		
		self.SetSizer( topsizer )
		self.Layout()
		
		# Connect Events
		self.Bind( wx.EVT_TOOL, self.add_functions, id = self.m_tool_add.GetId() )
		self.Bind( wx.EVT_TOOL, self.delete_functions, id = self.m_tool_delete.GetId() )
		self.Bind( wx.EVT_TOOL, self.take_function_up, id = self.m_tool_up.GetId() )
		self.Bind( wx.EVT_TOOL, self.take_function_down, id = self.m_tool_down.GetId() )
		self.Bind( wx.EVT_TOOL, self.save_change, id = self.m_tool_save.GetId() )
		self.Bind( wx.EVT_TOOL, self.redo_edit, id = self.m_tool_redo.GetId() )
	
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
	
	def redo_edit( self, event ):
		event.Skip()
	


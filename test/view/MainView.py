# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Aug  3 2017)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

from test.view.function_list.Panel_ChooseFunc_overwrite import Panel_ChooseFunc
from test.view.control_process.Panel_controlprocess_overwrite import panel_process
import wx
import wx.xrc

###########################################################################
## Class Frame_Main
###########################################################################

class Frame_Main ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		topsizer = wx.BoxSizer( wx.VERTICAL )
		
		self.panel_programming_Main = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		main_sizer = wx.FlexGridSizer( 0, 2, 0, 0 )
		main_sizer.AddGrowableCol( 1 )
		main_sizer.AddGrowableRow( 0 )
		main_sizer.SetFlexibleDirection( wx.BOTH )
		main_sizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.panel_functionlist = Panel_ChooseFunc( self.panel_programming_Main, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )
		main_sizer.Add( self.panel_functionlist, 0, wx.EXPAND, 5 )
		
		self.panel_controlprocess = panel_process( self.panel_programming_Main, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )
		main_sizer.Add( self.panel_controlprocess, 0, wx.EXPAND, 5 )
		
		self.panel_editparas = wx.Panel( self.panel_programming_Main, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )
		main_sizer.Add( self.panel_editparas, 0, wx.EXPAND, 5 )
		
		
		self.panel_programming_Main.SetSizer( main_sizer )
		self.panel_programming_Main.Layout()
		main_sizer.Fit( self.panel_programming_Main )
		topsizer.Add( self.panel_programming_Main, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( topsizer )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	


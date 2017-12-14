# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Aug  3 2017)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

from view_function_list.Panel_ChooseFunc_overwrite import Panel_ChooseFunc
from view_process.Panel_controlprocess_overwrite import panel_process
from view_parameters.Panel_control_paras_overwrite import panel_control_paras
import wx
import wx.xrc

###########################################################################
## Class Panel_luaprogramming
###########################################################################

class Panel_luaprogramming ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL )
		
		topsizer = wx.BoxSizer( wx.VERTICAL )
		
		self.panel_programming_Main = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.panel_functionlist = Panel_ChooseFunc( self.panel_programming_Main, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )
		bSizer2.Add( self.panel_functionlist, 0, wx.EXPAND, 5 )
		
		self.panel_controlprocess = panel_process( self.panel_programming_Main, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )
		bSizer2.Add( self.panel_controlprocess, 1, wx.EXPAND, 5 )
		
		self.panel_editparas = panel_control_paras( self.panel_programming_Main, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )
		self.panel_editparas.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )
		
		bSizer2.Add( self.panel_editparas, 1, wx.EXPAND, 5 )
		
		
		self.panel_programming_Main.SetSizer( bSizer2 )
		self.panel_programming_Main.Layout()
		bSizer2.Fit( self.panel_programming_Main )
		topsizer.Add( self.panel_programming_Main, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( topsizer )
		self.Layout()
	
	def __del__( self ):
		pass
	


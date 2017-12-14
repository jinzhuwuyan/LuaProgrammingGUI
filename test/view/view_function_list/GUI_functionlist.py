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
## Class Panel_ChooseFunc
###########################################################################

class Panel_ChooseFunc ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.TAB_TRAVERSAL )
		
		topsizer = wx.FlexGridSizer( 0, 2, 0, 0 )
		topsizer.AddGrowableCol( 0 )
		topsizer.AddGrowableRow( 0 )
		topsizer.SetFlexibleDirection( wx.BOTH )
		topsizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		m_listBox_choosefunctionChoices = [ u"1", u"2" ]
		self.m_listBox_choosefunction = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_listBox_choosefunctionChoices, wx.LB_ALWAYS_SB|wx.LB_SINGLE|wx.LB_SORT )
		topsizer.Add( self.m_listBox_choosefunction, 0, wx.EXPAND, 5 )
		
		
		self.SetSizer( topsizer )
		self.Layout()
		topsizer.Fit( self )
		
		# Connect Events
		self.m_listBox_choosefunction.Bind( wx.EVT_LISTBOX, self.update_func )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def update_func( self, event ):
		event.Skip()
	


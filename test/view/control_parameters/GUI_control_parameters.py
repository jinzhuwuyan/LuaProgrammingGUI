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
## Class panel_control_parameters
###########################################################################

class panel_control_parameters ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.TAB_TRAVERSAL )
		
		self.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		topsizer = wx.BoxSizer( wx.VERTICAL )
		
		
		self.SetSizer( topsizer )
		self.Layout()
		topsizer.Fit( self )
		
		# Connect Events
		self.Bind( wx.EVT_LEAVE_WINDOW, self.refresh_paras_panel )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def refresh_paras_panel( self, event ):
		event.Skip()
	

###########################################################################
## Class panel_control_paras
###########################################################################

class panel_control_paras ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.TAB_TRAVERSAL )
		
		topsizer = wx.BoxSizer( wx.HORIZONTAL )
		
		text_sizer = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText_paraname = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText_paraname.Wrap( -1 )
		text_sizer.Add( self.m_staticText_paraname, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.RIGHT, 5 )
		
		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		text_sizer.Add( self.m_staticText2, 0, wx.ALIGN_CENTER_VERTICAL|wx.BOTTOM|wx.RIGHT|wx.TOP, 5 )
		
		
		topsizer.Add( text_sizer, 1, wx.ALIGN_CENTER_VERTICAL, 5 )
		
		sizer_get_value = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_textCtrl_paravalue = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizer_get_value.Add( self.m_textCtrl_paravalue, 0, 0, 5 )
		
		self.m_bpButton_checkisNull = wx.BitmapButton( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( u"gtk-ok", wx.ART_BUTTON ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		sizer_get_value.Add( self.m_bpButton_checkisNull, 0, 0, 5 )
		
		
		topsizer.Add( sizer_get_value, 1, wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		self.SetSizer( topsizer )
		self.Layout()
		topsizer.Fit( self )
		
		# Connect Events
		self.m_textCtrl_paravalue.Bind( wx.EVT_KILL_FOCUS, self.check_isNull )
		self.m_textCtrl_paravalue.Bind( wx.EVT_SET_FOCUS, self.save_tmpvalue )
		self.m_textCtrl_paravalue.Bind( wx.EVT_TEXT, self.save_content )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def check_isNull( self, event ):
		event.Skip()
	
	def save_tmpvalue( self, event ):
		event.Skip()
	
	def save_content( self, event ):
		event.Skip()
	


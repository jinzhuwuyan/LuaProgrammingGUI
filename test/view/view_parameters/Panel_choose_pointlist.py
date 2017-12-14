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
## Class choose_pointlist
###########################################################################

class choose_pointlist ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL )
		
		topsizer = wx.FlexGridSizer( 2, 1, 0, 0 )
		topsizer.AddGrowableCol( 0 )
		topsizer.AddGrowableRow( 1 )
		topsizer.SetFlexibleDirection( wx.BOTH )
		topsizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		bSizer128 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText_pointlist = wx.StaticText( self, wx.ID_ANY, u"点列表：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_pointlist.Wrap( -1 )
		bSizer128.Add( self.m_staticText_pointlist, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		m_comboBox_pointlistChoices = []
		self.m_comboBox_pointlist = wx.ComboBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, m_comboBox_pointlistChoices, 0 )
		bSizer128.Add( self.m_comboBox_pointlist, 0, wx.BOTTOM|wx.EXPAND|wx.TOP, 5 )
		
		
		topsizer.Add( bSizer128, 0, wx.SHAPED|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		gSizer_showpos = wx.GridSizer( 8, 2, 0, 0 )
		
		self.m_staticText164 = wx.StaticText( self, wx.ID_ANY, u"位置", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText164.Wrap( -1 )
		gSizer_showpos.Add( self.m_staticText164, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText165 = wx.StaticText( self, wx.ID_ANY, u"值", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText165.Wrap( -1 )
		gSizer_showpos.Add( self.m_staticText165, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.m_staticText_X = wx.StaticText( self, wx.ID_ANY, u"X", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_X.Wrap( -1 )
		gSizer_showpos.Add( self.m_staticText_X, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.m_textCtrl_Xvalue = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCtrl_Xvalue.Enable( False )
		
		gSizer_showpos.Add( self.m_textCtrl_Xvalue, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText_Y = wx.StaticText( self, wx.ID_ANY, u"Y", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_Y.Wrap( -1 )
		gSizer_showpos.Add( self.m_staticText_Y, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.m_textCtrl_Yvalue = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCtrl_Yvalue.Enable( False )
		
		gSizer_showpos.Add( self.m_textCtrl_Yvalue, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText_Z = wx.StaticText( self, wx.ID_ANY, u"Z", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_Z.Wrap( -1 )
		gSizer_showpos.Add( self.m_staticText_Z, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.m_textCtrl_Zvalue = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCtrl_Zvalue.Enable( False )
		
		gSizer_showpos.Add( self.m_textCtrl_Zvalue, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText_U = wx.StaticText( self, wx.ID_ANY, u"U", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_U.Wrap( -1 )
		gSizer_showpos.Add( self.m_staticText_U, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.m_textCtrl_Uvalue = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCtrl_Uvalue.Enable( False )
		
		gSizer_showpos.Add( self.m_textCtrl_Uvalue, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText_V = wx.StaticText( self, wx.ID_ANY, u"V", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_V.Wrap( -1 )
		gSizer_showpos.Add( self.m_staticText_V, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.m_textCtrl_Vvalue = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCtrl_Vvalue.Enable( False )
		
		gSizer_showpos.Add( self.m_textCtrl_Vvalue, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText_W = wx.StaticText( self, wx.ID_ANY, u"W", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_W.Wrap( -1 )
		gSizer_showpos.Add( self.m_staticText_W, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.m_textCtrl_Wvalue = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCtrl_Wvalue.Enable( False )
		
		gSizer_showpos.Add( self.m_textCtrl_Wvalue, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		bSizer_elbow = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText_elbow = wx.StaticText( self, wx.ID_ANY, u"左右手：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_elbow.Wrap( -1 )
		bSizer_elbow.Add( self.m_staticText_elbow, 0, wx.ALL, 5 )
		
		m_choice_elbowChoices = [ u"左", u"右" ]
		self.m_choice_elbow = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 80,-1 ), m_choice_elbowChoices, 0 )
		self.m_choice_elbow.SetSelection( 0 )
		self.m_choice_elbow.Enable( False )
		
		bSizer_elbow.Add( self.m_choice_elbow, 0, 0, 5 )
		
		
		gSizer_showpos.Add( bSizer_elbow, 1, wx.EXPAND|wx.SHAPED|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		bSizer_handmode = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText_handmode = wx.StaticText( self, wx.ID_ANY, u"高低手：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_handmode.Wrap( -1 )
		bSizer_handmode.Add( self.m_staticText_handmode, 0, wx.ALL, 5 )
		
		m_choice_handmodeChoices = [ u"高", u"低" ]
		self.m_choice_handmode = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 80,-1 ), m_choice_handmodeChoices, 0 )
		self.m_choice_handmode.SetSelection( 0 )
		self.m_choice_handmode.Enable( False )
		
		bSizer_handmode.Add( self.m_choice_handmode, 0, 0, 5 )
		
		
		gSizer_showpos.Add( bSizer_handmode, 1, wx.EXPAND|wx.SHAPED|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		topsizer.Add( gSizer_showpos, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( topsizer )
		self.Layout()
		
		# Connect Events
		self.m_comboBox_pointlist.Bind( wx.EVT_COMBOBOX, self.choose_point )
		self.m_comboBox_pointlist.Bind( wx.EVT_TEXT, self.check_point )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def choose_point( self, event ):
		event.Skip()
	
	def check_point( self, event ):
		event.Skip()
	


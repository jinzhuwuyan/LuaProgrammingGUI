# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Aug  3 2017)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
from LuaProgrammingGUI.test.view.view_process.TreeMixin  import VirtualTreeListCtrl_ControlIF

###########################################################################
## Class If_Condition_Panel
###########################################################################

class If_Condition_Panel ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.TAB_TRAVERSAL )
		
		topsizer = wx.FlexGridSizer( 2, 1, 0, 0 )
		topsizer.AddGrowableCol( 0 )
		topsizer.AddGrowableRow( 1 )
		topsizer.SetFlexibleDirection( wx.BOTH )
		topsizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		head_sizer = wx.GridSizer( 4, 3, 0, 0 )
		
		self.m_radioBtn_allneed = wx.RadioButton( self, wx.ID_ANY, u"全部必须满足", wx.DefaultPosition, wx.DefaultSize, 0 )
		head_sizer.Add( self.m_radioBtn_allneed, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		head_sizer.Add( self.m_staticText4, 0, wx.ALL, 5 )
		
		self.m_radioBtn_onlyone = wx.RadioButton( self, wx.ID_ANY, u"满足任意一个", wx.DefaultPosition, wx.DefaultSize, 0 )
		head_sizer.Add( self.m_radioBtn_onlyone, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.m_staticText_ = wx.StaticText( self, wx.ID_ANY, u"条件", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_.Wrap( -1 )
		head_sizer.Add( self.m_staticText_, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"操作", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		head_sizer.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"值", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		head_sizer.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		m_choice_chooseconditionChoices = []
		self.m_choice_choosecondition = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_chooseconditionChoices, 0 )
		self.m_choice_choosecondition.SetSelection( 0 )
		head_sizer.Add( self.m_choice_choosecondition, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		m_choice_choosecontrolChoices = []
		self.m_choice_choosecontrol = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_choosecontrolChoices, 0 )
		self.m_choice_choosecontrol.SetSelection( 0 )
		head_sizer.Add( self.m_choice_choosecontrol, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		m_choice_choosevalueChoices = []
		self.m_choice_choosevalue = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_choosevalueChoices, 0 )
		self.m_choice_choosevalue.SetSelection( 0 )
		head_sizer.Add( self.m_choice_choosevalue, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_button_add = wx.Button( self, wx.ID_ANY, u"增加条件", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		head_sizer.Add( self.m_button_add, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT|wx.RIGHT, 5 )
		
		self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )
		head_sizer.Add( self.m_staticText7, 0, wx.ALL, 5 )
		
		self.m_button_delete = wx.Button( self, wx.ID_ANY, u"删除条件", wx.DefaultPosition, wx.DefaultSize, 0 )
		head_sizer.Add( self.m_button_delete, 0, wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		topsizer.Add( head_sizer, 0, wx.EXPAND, 5 )
		
		self.showconditiontree = VirtualTreeListCtrl_ControlIF(self, treemodel=self.ifcontrol.model, log=self.log)
		topsizer.Add( self.showconditiontree, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		self.SetSizer( topsizer )
		self.Layout()
		topsizer.Fit( self )
		
		# Connect Events
		self.m_radioBtn_allneed.Bind( wx.EVT_RADIOBUTTON, self.set_choose_mode )
		self.m_radioBtn_onlyone.Bind( wx.EVT_RADIOBUTTON, self.set_choose_mode )
		self.m_choice_choosecondition.Bind( wx.EVT_CHOICE, self.choose_condition )
		self.m_choice_choosecontrol.Bind( wx.EVT_CHOICE, self.choose_operation )
		self.m_choice_choosevalue.Bind( wx.EVT_CHOICE, self.choose_value )
		self.m_button_add.Bind( wx.EVT_BUTTON, self.add_condition )
		self.m_button_delete.Bind( wx.EVT_BUTTON, self.delete_condition )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def set_choose_mode( self, event ):
		event.Skip()
	
	
	def choose_condition( self, event ):
		event.Skip()
	
	def choose_operation( self, event ):
		event.Skip()
	
	def choose_value( self, event ):
		event.Skip()
	
	def add_condition( self, event ):
		event.Skip()
	
	def delete_condition( self, event ):
		event.Skip()
	


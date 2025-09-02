# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Mar 22 2011)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.grid

###########################################################################
## Class MyFrame1
###########################################################################

class MyFrame1 ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Lab Conditions Monitor", pos = wx.DefaultPosition, size = wx.Size( 1250,767 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		self.m_menubar1 = wx.MenuBar( 0 )
		self.m_menu2 = wx.Menu()
		self.m_menuItem1 = wx.MenuItem( self.m_menu2, wx.ID_ANY, u"Save graph to file", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu2.AppendItem( self.m_menuItem1 )
		
		self.m_menubar1.Append( self.m_menu2, u"Project" ) 
		
		self.SetMenuBar( self.m_menubar1 )
		
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_notebook1 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.m_panel2 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gSizer1 = wx.GridSizer( 0, 2, 0, 0 )
		
		fgSizer3 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer3.SetFlexibleDirection( wx.BOTH )
		fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText3 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Measure Controls", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		self.m_staticText3.SetFont( wx.Font( 12, 74, 90, 92, False, "Tahoma" ) )
		
		fgSizer3.Add( self.m_staticText3, 0, wx.ALL, 5 )
		
		self.m_staticText21 = wx.StaticText( self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText21.Wrap( -1 )
		fgSizer3.Add( self.m_staticText21, 0, wx.ALL, 5 )
		
		self.m_button1 = wx.Button( self.m_panel2, wx.ID_ANY, u"Single Measure", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer3.Add( self.m_button1, 0, wx.ALL, 5 )
		
		self.m_button2 = wx.Button( self.m_panel2, wx.ID_ANY, u"Stop Measure", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer3.Add( self.m_button2, 0, wx.ALL, 5 )
		
		self.m_button6 = wx.Button( self.m_panel2, wx.ID_ANY, u"Auto Measure", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer3.Add( self.m_button6, 0, wx.ALL, 5 )
		
		self.m_button5 = wx.Button( self.m_panel2, wx.ID_ANY, u"Stop Auto Measure", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer3.Add( self.m_button5, 0, wx.ALL, 5 )
		
		self.m_staticText6 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Auto interval", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		fgSizer3.Add( self.m_staticText6, 0, wx.ALL, 5 )
		
		m_choice2Choices = [ u"5", u"10", u"20", u"30" ]
		self.m_choice2 = wx.Choice( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice2Choices, 0 )
		self.m_choice2.SetSelection( 0 )
		fgSizer3.Add( self.m_choice2, 0, wx.ALL, 5 )
		
		self.m_button9 = wx.Button( self.m_panel2, wx.ID_ANY, u"Initialize all Instruments", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer3.Add( self.m_button9, 0, wx.ALL, 5 )
		
		gSizer1.Add( fgSizer3, 1, wx.EXPAND, 5 )
		
		fgSizer2 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText2 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Graph Controls", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		self.m_staticText2.SetFont( wx.Font( 11, 74, 90, 92, False, "Tahoma" ) )
		
		fgSizer2.Add( self.m_staticText2, 0, wx.ALL, 5 )
		
		self.m_staticText4 = wx.StaticText( self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		fgSizer2.Add( self.m_staticText4, 0, wx.ALL, 5 )
		
		self.m_button3 = wx.Button( self.m_panel2, wx.ID_ANY, u"Single Draw", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer2.Add( self.m_button3, 0, wx.ALL, 5 )
		
		self.m_button4 = wx.Button( self.m_panel2, wx.ID_ANY, u"Stop Draw", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer2.Add( self.m_button4, 0, wx.ALL, 5 )
		
		self.m_button7 = wx.Button( self.m_panel2, wx.ID_ANY, u"Auto Draw", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer2.Add( self.m_button7, 0, wx.ALL, 5 )
		
		self.m_button8 = wx.Button( self.m_panel2, wx.ID_ANY, u"Stop Auto Draw", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer2.Add( self.m_button8, 0, wx.ALL, 5 )
		
		self.m_staticText7 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Auto interval", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )
		fgSizer2.Add( self.m_staticText7, 0, wx.ALL, 5 )
		
		m_choice3Choices = [ u"5", u"10", u"20", u"30" ]
		self.m_choice3 = wx.Choice( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice3Choices, 0 )
		self.m_choice3.SetSelection( 0 )
		fgSizer2.Add( self.m_choice3, 0, wx.ALL, 5 )
		
		self.Scroll = wx.CheckBox( self.m_panel2, wx.ID_ANY, u"Scrolling", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer2.Add( self.Scroll, 0, wx.ALL, 5 )
		
		length_choiceChoices = [ u"50", u"150", u"300", u"2000", u"8000" ]
		self.length_choice = wx.Choice( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, length_choiceChoices, 0 )
		self.length_choice.SetSelection( 0 )
		fgSizer2.Add( self.length_choice, 0, wx.ALL, 5 )
		
		gSizer1.Add( fgSizer2, 1, wx.EXPAND, 5 )
		
		self.m_textCtrl1 = wx.TextCtrl( self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 300,300 ), wx.TE_MULTILINE )
		gSizer1.Add( self.m_textCtrl1, 0, wx.ALL, 5 )
		
		fgSizer31 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer31.SetFlexibleDirection( wx.BOTH )
		fgSizer31.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText5 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Data Files", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.m_staticText5.Wrap( -1 )
		self.m_staticText5.SetFont( wx.Font( 12, 74, 90, 92, False, "Tahoma" ) )
		
		fgSizer31.Add( self.m_staticText5, 0, wx.ALL, 5 )
		
		self.m_grid1 = wx.grid.Grid( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		
		# Grid
		self.m_grid1.CreateGrid( 8, 2 )
		self.m_grid1.EnableEditing( True )
		self.m_grid1.EnableGridLines( True )
		self.m_grid1.EnableDragGridSize( False )
		self.m_grid1.SetMargins( 0, 0 )
		
		# Columns
		self.m_grid1.SetColSize( 0, 122 )
		self.m_grid1.SetColSize( 1, 200 )
		self.m_grid1.EnableDragColMove( False )
		self.m_grid1.EnableDragColSize( True )
		self.m_grid1.SetColLabelSize( 30 )
		self.m_grid1.SetColLabelValue( 0, u"Channel" )
		self.m_grid1.SetColLabelValue( 1, u"File name" )
		self.m_grid1.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Rows
		self.m_grid1.EnableDragRowSize( True )
		self.m_grid1.SetRowLabelSize( 80 )
		self.m_grid1.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Label Appearance
		
		# Cell Defaults
		self.m_grid1.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		fgSizer31.Add( self.m_grid1, 0, wx.ALL, 5 )
		
		gSizer1.Add( fgSizer31, 1, wx.EXPAND, 5 )
		
		self.m_panel2.SetSizer( gSizer1 )
		self.m_panel2.Layout()
		gSizer1.Fit( self.m_panel2 )
		self.m_notebook1.AddPage( self.m_panel2, u"Controls", True )
		self.m_panel1 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_notebook1.AddPage( self.m_panel1, u"Graph", False )
		
		bSizer3.Add( self.m_notebook1, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.SetSizer( bSizer3 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_MENU, self.OnSaveGraph, id = self.m_menuItem1.GetId() )
		self.m_button1.Bind( wx.EVT_BUTTON, self.OnButton1 )
		self.m_button2.Bind( wx.EVT_BUTTON, self.OnButton2 )
		self.m_button6.Bind( wx.EVT_BUTTON, self.OnStartTimer1 )
		self.m_button5.Bind( wx.EVT_BUTTON, self.OnStopTimer1 )
		self.m_button9.Bind( wx.EVT_BUTTON, self.OnInitialize )
		self.m_button3.Bind( wx.EVT_BUTTON, self.OnButton3 )
		self.m_button4.Bind( wx.EVT_BUTTON, self.OnButton4 )
		self.m_button7.Bind( wx.EVT_BUTTON, self.OnStartTimer2 )
		self.m_button8.Bind( wx.EVT_BUTTON, self.OnStopTimer2 )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnSaveGraph( self, event ):
		event.Skip()
	
	def OnButton1( self, event ):
		event.Skip()
	
	def OnButton2( self, event ):
		event.Skip()
	
	def OnStartTimer1( self, event ):
		event.Skip()
	
	def OnStopTimer1( self, event ):
		event.Skip()
	
	def OnInitialize( self, event ):
		event.Skip()
	
	def OnButton3( self, event ):
		event.Skip()
	
	def OnButton4( self, event ):
		event.Skip()
	
	def OnStartTimer2( self, event ):
		event.Skip()
	
	def OnStopTimer2( self, event ):
		event.Skip()
	


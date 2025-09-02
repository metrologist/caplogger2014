# Implementing MyFrame1
import sys
import wx
import date_gui
import time

class RedirectText(object):
    def __init__(self, aWxTextCtrl):
            self.out = aWxTextCtrl
    def write(self, string):
            self.out.WriteText(string)

class ProjectFrame( date_gui.MyFrame1 ):
    def __init__( self, parent ):
            date_gui.MyFrame1.__init__( self, parent)
            redir = RedirectText(self.m_textCtrl1)
            sys.stdout = redir
            sys.stderr = redir
            self.Show()
            
    def onPlot(self,event):
        print 'hello from start'
        x = wx.DateTime.Now()
        print x
        b = wx.TimeSpan.Days(7) # for range back 1 week
        c = wx.TimeSpan.Days(1) # for range up to at least end of day
        a = self.m_calendar1.GetDate()
        print a.GetTicks()
        print a

        print 'hello from finish'
        a = self.m_calendar2.GetDate()
        print a.GetTicks()
        print a
        self.m_calendar1.SetDate(a)
        print 'time now'
        print time.time()
        self.m_calendar1.SetDate(wx.DateTime.SubtractTS(a, b))
        self.m_calendar2.SetDate(x)
        print self.m_calendar2.GetDate().GetTicks()
	

if __name__ == "__main__":
    app = wx.App()
    ProjectFrame(None)
    app.MainLoop()
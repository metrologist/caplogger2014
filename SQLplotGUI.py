"""
Calendar GUI for selecting start and finish times for plotting capacitance
environment logs.
"""
# Implementing MyFrame1
import sys
import wx
import date_gui
import time
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg
import sqlite3

import matplotlib.pyplot as plt

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
            
            self.CreateGraph(self.m_panel3, "time / s", 8)
            self.Show()
            x,y = self.GetSize()
            self.SetSize((x-200, y-1))
            self.SetSize((x, y))
            
            x = wx.DateTime.Now()
            b = wx.TimeSpan.Days(1)
            self.m_calendar1.SetDate(wx.DateTime.SubtractTS(x, b))# set to yesterday
            
    def onPlot(self,event):
        print 'Getting data'
        x = wx.DateTime.Now()
        b = wx.TimeSpan.Days(7) # for range back 1 week
        c = wx.TimeSpan.Days(1) # for range up to at least end of day
        
        a1 = self.m_calendar1.GetDate()
        then = a1.GetTicks()

        aa = self.m_calendar2.GetDate()
        a2 = wx.DateTime.AddTS(aa,c) # add a day to take it to midnight
        then = a1.GetTicks()
        now = a2.GetTicks()
        print 'then = ',then
        print 'now = ',now
        self.PlotGraph(then, now)

    def CreateGraph(self, panel, xlabel, number):
        """
        Note use of pyplot for convenient subplots. Could be done in other ways.
        """
        panel.dpi = 100
        panel.fig, panel.axs = plt.subplots(number, 1,sharex=True , sharey=False)
        panel.axs[0].set_title('Capacitor Environment')
        panel.fig.set_facecolor('white')
        for i in range(number):
            panel.axs[i].set_axis_bgcolor('white')
            panel.axs[i].grid(True, color = 'black')
            panel.axs[i].tick_params(axis = 'both', labelsize = 8)
        panel.fig.tight_layout()        
        panel.canvas = FigureCanvas(panel, -1, panel.fig)
        panel.sizer = wx.BoxSizer(wx.VERTICAL)
        panel.sizer.Add(panel.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        panel.SetSizer(panel.sizer)
        self.add_2Dtoolbar(self.m_panel3)
        panel.Fit()
        
    def add_2Dtoolbar(self, panel):
        panel.toolbar = NavigationToolbar2WxAgg(panel.canvas)
        panel.toolbar.Realize()
        tw, th = panel.toolbar.GetSizeTuple()
        fw, fh = panel.canvas.GetSizeTuple()
        panel.toolbar.SetSize(wx.Size(fw, th))
        panel.sizer.Add(panel.toolbar, 0, wx.LEFT | wx.EXPAND)
        # update the axes menu on the toolbar
        panel.toolbar.update()
        
    def PlotGraph(self, then, now):
        alpha = 0.00385 # for quick conversion to temperature
        db_name = "dist\\cap_environment_2012_on.db"
        
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        sql = "SELECT name FROM sqlite_master WHERE type = 'table'" #ORDER BY name"
        cursor.execute(sql)
        tables = cursor.fetchall()

        i = 0
        for table in tables:
            sql = "SELECT time, value FROM " + table[0]+ " WHERE time BETWEEN "+ repr(then) +" AND " + repr(now)
            cursor.execute(sql)
            rowset = cursor.fetchall()
            cx = []
            cy = []
            for row in rowset:
                cx.append(row[0])
                cy.append(row[1])
            print table[0] #table name is a tuple, just want the name!
            self.m_panel3.axs[i].cla()
            self.m_panel3.axs[i].set_ylabel(table[0], size ='x-small')

            # all the time/date stuff needs more thought!!!
            if time.localtime(time.time()).tm_isdst==0:#this flag is set by the localtime call?#time.daylight ==0: # for computer time at this instant.
                offset = time.timezone # NZST
            else:
                offset = time.altzone # NZDT

            times = [(b - offset*0)/(24.0*3600)+1969*365.25 - 14.0 + 0.291666666628 for b in cx] #matplotlib prefers decimal days
            if i == 7:
                values = cy # for pressure
            else:
                values = [(b-100.0)/(100.0*alpha) for b in cy]
            self.m_panel3.axs[i].plot_date( times, values, 'g')   
            i = i + 1

        self.m_panel3.fig.autofmt_xdate() # rotates labels for clarity
        self.m_panel3.fig.tight_layout()
        self.m_panel3.fig.subplots_adjust( hspace = 0.1)
        self.m_panel3.canvas.draw()
        
        if conn:
            conn.close()

if __name__ == "__main__":
    app = wx.App()
    ProjectFrame(None)
    app.MainLoop()
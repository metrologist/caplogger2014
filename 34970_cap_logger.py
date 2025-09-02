"""
31 January 2013 version.
Trying to sort out threading with a GUI in anticipation of a GPIB program.
I intend having the GPIB and data processing in separate threads and using the
GUI thread for accessing common data files and displaying plots. A process such
as manual bridge balances can also just be another thread. This would allow for
reliable picking up of time stamped temperature/pressure data without having
to post process the environmental condition logs.
Now want to use the threading module and play with locks.
"""
import os
import sys
import time
import threading
import wx
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
#import matplotlib.dates as mdates
import noname  #default file from wxFormbuilder
import stuff #useful classes
import instruments2 #everything on the GPIB
import graphing #drawing the strip charts


# Define notification event for thread completion
EVT_RESULT_ID_1 = wx.NewId() #used for GPIB thread measuring sensors
EVT_RESULT_ID_2 = wx.NewId() #used for graphing thread
EVT_RESULT_ID_3 = wx.NewId() #used for GPIB thread that initialises instruments
      

# Implementing MyFrame1
class ProjectFrame( noname.MyFrame1 ):
    def __init__( self, parent ):
        noname.MyFrame1.__init__( self, parent)
        self.data = stuff.SharedList(None) #no data on start up
        self.dummy = stuff.SharedList(None) #for worker thread with dummy data
        self.number = 7 #number of channels, without druck
        self.CreateGraph(self.m_panel1, "time / s", self.number) # alternative for testing
        self.Show(True)
        x,y = self.GetSize()
        self.SetSize((x-200, y-1))
        self.SetSize((x, y))        
        # Set up event handler for any worker thread results
        stuff.EVT_RESULT(self,self.OnResult1, EVT_RESULT_ID_1)
        stuff.EVT_RESULT(self, self.OnResult2, EVT_RESULT_ID_2)
        stuff.EVT_RESULT(self, self.OnResult3, EVT_RESULT_ID_3)
        # And indicate we don't have a worker thread yet
        self.worker1 = None
        self.worker2 = None
        self.worker3 = None
        self.timer1 =wx.Timer(self) #a timer for data logging scheduling
        self.Bind(wx.EVT_TIMER, self.OnTimer1, self.timer1) # bind to OnTimer
        self.timer2 =wx.Timer(self) #a timer for data logging scheduling
        self.Bind(wx.EVT_TIMER, self.OnTimer2, self.timer2) # bind to OnTimer
        self.m_button5.Enable(False)
        self.m_button8.Enable(False)
        log = self.m_textCtrl1 # where stdout will be redirected
        redir = stuff.RedirectText(log)
        sys.stdout = redir
        sys.stderr = redir
        self.channels = ['Reference', 'S ball', 'Cropico temp', 'AH11', 'GR inner', 'GR outer', 'Permutable']
        self.files = ['data\\ref.csv', 'data\\s_ball.csv', 'data\\ref_temp.csv', 'data\\ah11.csv', 'data\\GR_inner.csv', 'data\\GR_outer.csv', 'data\\permutable.csv']
        self.FileGrid() # list of channels and files displayed in wxGrid
        self.cwd = os.getcwd() #defaults to the data directory being in the initial current working directory, note that a file dialog could later change the working directory
        
    def FileGrid(self):
        # ultimately will allow the user to enter file info on the grid as required
        for i in range(len(self.channels)):
            self.m_grid1.SetCellValue(i, 0, self.channels[i])
            self.m_grid1.SetCellValue(i, 1, self.files[i])

        
    def OnInitialize(self, evt):
        self.Initialize()
        
    def Initialize(self):
        """Reset GPIB instruments"""
        self.ButtonPrint("Reset underway")
        # Trigger the worker thread unless it's already busy
        if not (self.worker3 and self.worker1):
            self.worker3 = instruments2.GPIBStart(self, EVT_RESULT_ID_3, 1, self.dummy)        
    
    def OnTimer1(self, evt):
        if not self.worker1:
            self.doButton1()
            
    def OnStartTimer1(self,evt):
        #the options should be made to set the choice labels in the GUI
        options = {'0' : 5, '1' : 10, '2' : 20, '3' : 30} # dictionary
        mins = options[repr(self.m_choice2.GetSelection())]
        self.timer1.Start(mins*60000) #start the timer (not UTC synched!)
        self.m_button6.Enable(False)
        self.m_button5.Enable(True)
            
    def OnStopTimer1(self, evt): # panel button
        self.timer1.Stop()
        self.m_button6.Enable(True)
        self.m_button5.Enable(False)

    def OnTimer2(self, evt):
        if not self.worker2:
            self.doButton3()
            
    def OnStartTimer2(self,evt):
        self.doStartTimer2()
        
    def doStartTimer2(self):
        #the options should be made to set the choice labels in the GUI
        options = {'0' : 5, '1' : 10, '2' : 20, '3' : 30} # dictionary
        mins = options[repr(self.m_choice3.GetSelection())]        
        self.timer2.Start(mins*60000) #start the timer (not UTC synched!)
        #allowing to slip on purpose to see if any clashes occur
        self.m_button7.Enable(False)
        self.m_button8.Enable(True)            
        
    def OnStopTimer2(self, evt): # panel button
        self.doStopTimer2()
        
    def doStopTimer2(self):
        self.timer2.Stop()
        self.m_button7.Enable(True)
        self.m_button8.Enable(False)

    def CreateGraph(self, panel, xlabel, number):
        """
        Note use of pyplot for convenient subplots. Could be done in other ways.
        """
        panel.dpi = 100
        panel.fig, panel.axs = plt.subplots(number, 1,sharex=True , sharey=False)
        panel.axs[0].set_title('Capacitor Environment')
        for i in range(number):
            panel.axs[i].set_axis_bgcolor('black')
            panel.axs[i].grid(True, color = 'white')
            panel.axs[i].tick_params(axis = 'both', labelsize = 8)
        panel.fig.tight_layout()        
        panel.canvas = FigureCanvas(panel, -1, panel.fig)
        panel.sizer = wx.BoxSizer(wx.VERTICAL)
        panel.sizer.Add(panel.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        panel.SetSizer(panel.sizer)
        panel.Fit()

    def OnButton1(self, event):
        self.doButton1()#do what Button1 does!

    def doButton1(self): #what Button1 does
        """Start Computation."""
        # Trigger the worker thread unless it's already busy
        self
        if not (self.worker1 and self.worker3):
            self.ButtonPrint('Starting GPIB measure')
            self.worker1 = instruments2.GPIBThread(self, EVT_RESULT_ID_1, [self.number, self.files, self.cwd], self.data)

    def OnButton2(self, event):
        """Stop Computation."""
        # Flag the worker thread to stop if running
        if self.worker1:
            self.ButtonPrint('Trying to abort GPIB measure')
            self.worker1.abort()

    def OnButton3(self, event):
        self.doButton3()

    def doButton3(self):
        """Start Computation."""
        # Trigger the worker thread unless it's already busy
        if not self.worker2:
            self.ButtonPrint('Starting graphing')
            options = {'0' : 50, '1' : 150, '2' : 300, '3' : 2000, '4' : 8000} # dictionary
            plot_style = [self.Scroll.GetValue(), options[repr(self.length_choice.GetSelection())]]
            self.worker2 = graphing.DisplayThread(self, EVT_RESULT_ID_2, [self.number,self.m_panel1, plot_style], self.data)
 
    def OnButton4(self, event):
        self.doButton4()
        
    def doButton4(self):
        """Stop Computation."""
        # Flag the worker thread to stop if running
        if self.worker2:
            self.ButtonPrint('Trying to abort graphing')
            self.worker2.abort()

    def OnResult1(self, event):
        """Show Result status."""
        if event.data is None:
            # Thread aborted (using our convention of None return)
            print'GPIB measure aborted', time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        else:
            # Process results here
            print'Thread Result: %s' % event.data, time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())

        # In either event, the worker is done
        self.worker1 = None
 
    def OnResult2(self, event):
        """Show Result status."""
        if event.data is None:
            # Thread aborted (using our convention of None return)
            print'Graphing aborted', time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        else:
            # Process results here
            print'Graph Result: %s' % event.data,time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        # In either event, the worker is done
        self.worker2 = None

    def OnResult3(self, event):
        """Show Result status."""
        if event.data is None:
            # Thread aborted (using our convention of None return)
            print'Initialization aborted', time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        else:
            # Process results here
            print'Initialization Result: %s' % event.data, time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        # In either event, the worker is done
        self.worker3 = None
        
    def ButtonPrint(self, x):
        """
        Announces in the text window that an event has occured.  Intended for
        use by the GUI only, but could now be done with the redirected stdout.
        """
        self.m_textCtrl1.AppendText(x +'\n')
        
        
    def OnSaveGraph(self, event):
        """
        OnSaveGraph must halt the display thread and timer before saving the
        image.  Full Matplotlib toolbar not needed.
        """
        but7 = self.m_button7.IsEnabled()
        
        if not but7:
            self.doStopTimer2() #turn the timer off if it was running

        self.doButton4()# also abort the graph thread, just in case
        
        file_choices = "PNG (*.png)|*.png"
        
        dlg = wx.FileDialog(
            self, 
            message="Save plot as...",
            defaultDir=os.getcwd(),
            defaultFile="plot.png",
            wildcard=file_choices,
            style=wx.SAVE)
        
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.m_panel1.canvas.print_figure(path, dpi=self.m_panel1.dpi)
            self.ButtonPrint("Saved to %s" % path)
            
        if not but7:
            self.doStartTimer2() #turn the timer back on if it was running before saving
            

if __name__ == "__main__":
    app = wx.App()
    ProjectFrame(None)
    app.MainLoop()
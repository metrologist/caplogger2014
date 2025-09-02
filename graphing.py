"""
Draws the stripcharts as set up on the 'Graph' tab in the main program.
"""

import stuff
import time
import wx

class DisplayThread(stuff.WorkerThread):
    """
    Plots the data for the number of channels given in param[0] on the panel
    given in param[1], with plotting style given in param[3].
    """    
    def __init__(self, notify_window, EVT, param, data):
        stuff.WorkerThread.__init__(self, notify_window, EVT, param, data)

    def run(self):
        alpha = 0.00385 # for quick conversion to temperature
        #set up the axes and title each time
        y_label_list = ['Reference', 'S ball', 'Cropico temp', 'AH11', 'GR inner', 'GR outer', 'Permutable']
        for i in range(self.param[0]):
            self.param[1].axs[i].cla()
            self.param[1].axs[i].set_axis_bgcolor('black')
            self.param[1].axs[i].grid(True, color = 'white')
            self.param[1].axs[i].tick_params(axis = 'both', labelsize = 8)
            self.param[1].axs[i].set_ylabel(y_label_list[i], size ='x-small')
            self.param[1].axs[i].ticklabel_format(axis = 'y', style = 'plain', useOffset = False )
        self.param[1].axs[0].set_title('Capacitor Environment')
        
        x = self.data.copy_list() # want a copy of the list that doesn't change in length
        no_of_points = len(x)
        if self.param[2][0]:#if scroll is checked
            if no_of_points > self.param[2][1]: # and there are more points than needed
                a = x[-self.param[2][1]:]
            else:
                a = x
        else:
            a = x
            
        #this will plot data in local daylight or standard time
        #but note for plotting historic data (from file) might need to use pytz to determine if NZDT or NZST applies
        if time.localtime(time.time()).tm_isdst==0:#this flag is set by the localtime call?#time.daylight ==0: # for computer time at this instant.
            offset = time.timezone # NZST
        else:
            offset = time.altzone # NZDT
        for i in range(self.param[0]):
            times = [(b[i][0] - offset*0)/(24.0*3600)+1969*365.25 - 14.0 + 0.291666666628 for b in a] #matplotlib prefers decimal days
            if i == 7:
                skip()#was for druck
##                 values = [b[i][1] for b in a] # for pressure
            else:
                values = [(b[i][1]-100.0)/(100.0*alpha) for b in a]
            self.param[1].axs[i].plot_date( times, values, 'y')
        

        self.param[1].fig.autofmt_xdate() # rotates labels for clarity
        self.param[1].fig.tight_layout()
        self.param[1].fig.subplots_adjust( hspace = 0.1)       
        self.param[1].canvas.draw()
        
        time.sleep(0.1)
        
        if self._want_abort: #abort not useful for this single run thread
            wx.PostEvent(self._notify_window, stuff.ResultEvent(self.EVT, None))
            return
        wx.PostEvent(self._notify_window, stuff.ResultEvent(self.EVT, 'Plotting finished'))


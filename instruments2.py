"""
Everything about GPIB control. The GUI can only allow one GPIB thread at a time.
Otherwise difficult to see how the GPIB card can be kept thread safe.  Ultimately
might sort all this out in a single class with different methods for initialisation,
dummy data and data gathering operation.
"""

import stuff
import time
import wx
import visa
## import visa2 as visa #for running without instruments
import csv
import os
import sqlite3

class GPIBThread(stuff.WorkerThread):
    """
    Runs the instruments to gather 'data', communicating to the 'notify_window'
    and returning a [time, value] tuple for each of the 'param[0]' channels.
    param[0] is the number of channels, param[1] is a list of csv file names and
    param[2] is the initial working directory.
    """
    def __init__(self, notify_window, EVT, param, data):
        stuff.WorkerThread.__init__(self, notify_window, EVT, param, data)

    def file_write(self, parameters, index, item_time,item):
        """
        Adds timestamped item to file from parameters/index
        """
        f = open(os.path.join(self.param[2],self.param[1][index]), 'ab') # file chosen from param[1] file list
        writer = csv.writer(f)
        writer.writerow([item_time, item])
        f.flush()
        f.close()        
    
    def run(self):
        print 'Starting resistance measurement', time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        #copied parameters on the HP34970, should pass in!!!
        rnge = 100 #ohm
        res = 8.0e-7*rnge #ohm, PLC = 20
        PLC = 20.0 #p 203 of manual, linked to resolution
        avg = 9 # number of samples to average
        read_delay = PLC*0.02*2.0 #time to take reading at selected resolution
        settle = 18 # number of readings to allow resistor to heat/settle
        
        # set up link to database
##         db_name = "cap_env_Jan2013.db"
##        db_name = "cap_environment_August_2019_on.db"
##        db_name = "cap_environment_September_2021_on.db"
	db_name = "cap_environment_May_2022_on.db"
        table_names = ['Reference', 'S_ball', 'Cropico_temp', 'AH11', 'GR_inner', 'GR_outer', 'Permutable']
        conn =sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        try:
            logger = visa.GpibInstrument('GPIB::9')
        except visa.VisaIOError:
            print 'Failing to find HP34970', time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
            wx.PostEvent(self._notify_window, stuff.ResultEvent(self.EVT, None))
            return
        a = []
        k = 0 # channel counter
        counter = 0
        for i in [1, 2, 3, 5, 6, 7, 8]: #note missing channel 4
            try:
                if counter <=6:
                    display_command = "DISP:TEXT '"+ table_names[counter]+ "'"
                    logger.write(display_command) # front panel display
                logger.write('ROUT:SCAN (@10' + repr(i) + ')')
                logger.write('TRIG:SOUR IMM') # accept immediate trigger, idle
                counter+=1
            except visa.VisaIOError:
                print 'Failing to write to HP34970 i= ', i,' ', time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
                wx.PostEvent(self._notify_window, stuff.ResultEvent(self.EVT, None))
                return
            try:
                result = []
                for j in range(settle):
                    logger.write('READ?') # trigger armed
                    time.sleep(read_delay)
                    if self._want_abort:
                        wx.PostEvent(self._notify_window, stuff.ResultEvent(self.EVT, None))
                        return
                    result.append(float(logger.read_values()[0]))    

                if len(result) < avg:
                    average = float(sum(result)/len(result))
                else:
                    average = float(sum(result[-avg:])/avg)
                time_stamp = time.time()
                self.file_write(self.param, k, time_stamp, average)# save to file
                a.append((time_stamp, average))# save to memory
                command = "INSERT INTO " + table_names[k] + " VALUES(?,?)"
                cursor.execute(command, [time_stamp, average])
                k = k + 1 #increment channel counter
                print time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()), i, average
            except visa.VisaIOError:
                print 'Failing to read from HP34970', time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
                wx.PostEvent(self._notify_window, stuff.ResultEvent(self.EVT, None))
                return
##         if self.druck ==1:
##             try:        
##                 pressure = visa.GpibInstrument('GPIB::16')
##                 result = pressure.read_values()[0]
##             except visa.VisaIOError:
##                 print 'Failing to communicate with Druck', time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
##                 wx.PostEvent(self._notify_window, stuff.ResultEvent(self.EVT, None))
##                 return            
##             time_stamp =time.time()
##             self.file_write(self.param, k, time_stamp, result)        
##             a.append((time_stamp, result))
##             command = "INSERT INTO " + table_names[k] + " VALUES(?,?)"
##             cursor.execute(command, [time_stamp, result])
        conn.commit() #all database additions made final and visible
        print time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()), i, average
        self.data.add_to_list(a)
        logger.write("DISP:TEXT 'Paused'") # front panel display
        wx.PostEvent(self._notify_window, stuff.ResultEvent(self.EVT, 'GPIB halted'))
        


class GPIBStart(stuff.WorkerThread):
    """
    Wakes up GPIB for the first time.
    """
    def __init__(self, notify_window, EVT, param, data):
        stuff.WorkerThread.__init__(self, notify_window, EVT, param, data)
        self.druck = 1 # assume druck is available
    def run(self):
        try:
            check = visa.get_instruments_list()
        except visa.VisaIOError:
            wx.PostEvent(self._notify_window, stuff.ResultEvent(self.EVT, None))
            return
        print check
        if 'GPIB0::9' in check:            
            try:
                logger = visa.GpibInstrument('GPIB::' + '9')
                #logger.write('*RST') #reset HP34970 to a defined state
                logger.write("DISP:TEXT 'MYVISA'") # front panel display
            except visa.VisaIOError:
                wx.PostEvent(self._notify_window, stuff.ResultEvent(self.EVT, None))
                return
            print 'HP34970 reset'
        else:
            print 'Can not find the HP34970'
            wx.PostEvent(self._notify_window, stuff.ResultEvent(self.EVT, None))
            return
        
##         if 'GPIB0::16' in check:
##             print 'Druck DPI 141 available'
##         else:
##             self.druck = 0 #no druck available
##             print 'Druck DPI 141 not found'
##             wx.PostEvent(self._notify_window, stuff.ResultEvent(self.EVT, None))
##             return
            
        #set up parameters on the HP34970
        rnge = 100 #ohm
        res = 8.0e-7*rnge #ohm, PLC = 20
        PLC = 20.0 #p 203 of manual, linked to resolution
        settling = 30 #time to allow resistor to settle at current
        read_delay = PLC*0.02*2.0 #time to take reading at selected resolution
        try:
            for i in range(8): #set all 8 channels identically
                channel = '(@10' + repr(i+1)+ ')'
                logger.write("CONF:FRES " + str(rnge) +", " + str(res) + ', ' + channel)
                logger.write("FRES:OCOM ON, " + channel)
        except visa.VisaIOError:
            wx.PostEvent(self._notify_window, stuff.ResultEvent(self.EVT, None))
            return        
            
        wx.PostEvent(self._notify_window, stuff.ResultEvent(self.EVT, 'GPIB reset'))

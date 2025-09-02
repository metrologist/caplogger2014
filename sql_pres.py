#sql_pres is similar to sql_cap but for dealing with pressure from the room logging system
import sqlite3
from dateutil import parser
from matplotlib import pyplot as plt
from matplotlib import dates as mdates
import os
from intertime import INTERTIME
import numpy as np
from GTC import ureal

class SQLDATA_P():
    def __init__(self, source):
        """

        Accesses the sqlite database created by the room logger system on linux.
        Output is ultimately .jpg and .pdf files in \LoggerData\temperature_figs
        :param source:  string file name as in '\LoggerData\name.db'
        """
        self.t = INTERTIME('Pacific/Auckland')  # could be a parameter, but only used here
        self.source = source  # note that the source could be entered at the get_info method instead of the class
        self.wd = os.getcwd()  # get working directory

    def get_info(self, begin, end):
        """

        :param begin: naive string datetime, assumed local time
        :param end: naive string datetime, assumed local time
        :return: dictionary {'Table name': result_dict} of result dictionaries {'dat_range':, 'time':, 'mean_time':,
         'temp':, 'mean_temp':, 'sd_temp':}
        """
        begin = self.t.local_to_sql_UTC(begin)  # bad way to make available to the plot!
        end = self.t.local_to_sql_UTC(end)
        start_string = begin
        finish_string = end
        selected_db = self.source
        db_path = os.path.join(self.wd, selected_db)
        file_exists = os.path.exists(db_path)  # check it exists to avoid creating a blank
        if file_exists:
            conn = sqlite3.connect(selected_db)  # note the risk it will create one if it can't be found
            cursor = conn.cursor()
            start = start_string
            finish = finish_string
            sql = "SELECT timestamp, P FROM " + 'Druck_data' + " WHERE timestamp BETWEEN " + repr(start) + " AND " + repr(finish)
            cursor.execute(sql)
            rowset = cursor.fetchall()
            cx = []
            cy = []
            for row in rowset:
                a = parser.parse(row[0])  # naive time, essentially UTC?
                a = self.t.datetime_to_decimal_year(a)  # convert to decimal UTC
                cx.append(a)  # decimal year for a simple plot
                cy.append(row[1])  # pressure for plotting
            mean_time = np.mean(cx)  # mean decimal year
            mean_date = self.t.decimal_year_to_datetime(mean_time)  # as local time_date
            mean_press = np.mean(cy)
            stdev_press = np.std(cy)
            # print(mean_time)
            print('mean_date')
            print(mean_date)
            print('mean_press')
            print(mean_press)
            print('stdev_press')
            print(stdev_press)
            print()
        else:
            mean_press, stdev_press = 0, 0
        return mean_press, stdev_press

if __name__ == '__main__':
    date_tuples_2 = [
        ('3 July, 2025, 1:00 AM', '3 July, 2025, 4:00 PM'),
        ('4 July, 2025, 9:00 AM', '4 July, 2025, 4:00 PM'),
        ('7 July, 2025, 9:00 AM', '7 July, 2025, 4:00 PM'),
        ('8 July, 2025, 9:00 AM', '8 July, 2025, 4:00 PM'),
        ('11 July, 2025, 9:00 AM', '11 July, 2025, 4:00 PM'),
        ('23 October, 2025, 9:00 AM', '23 October, 2025, 4:00 PM'),
        ('28 October, 2025, 9:00 AM', '28 October, 2025, 4:00 PM'),
        ('3 November, 2025, 9:00 AM', '3 November, 2025, 4:00 PM'),
        ('6 November, 2025, 9:00 AM', '6 November, 2025, 4:00 PM'),
        ('21 November, 2025, 9:00 AM', '21 November, 2025, 4:00 PM'),
        ('1 December, 2025, 9:00 AM', '1 December, 2025, 4:00 PM'),
        ('5 December, 2025, 9:00 AM', '5 December, 2025, 4:00 PM')
                     ]
    sql = SQLDATA_P('LoggerData\druck.db')
    for x in date_tuples_2:
        pressure, stdev = sql.get_info(x[0], x[1])

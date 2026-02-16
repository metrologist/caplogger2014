# sql_cap.py presents the caplogger values in a given date range
import sqlite3
from matplotlib import pyplot as plt
from matplotlib import dates as mdates
import os
from intertime import INTERTIME
import numpy as np
from GTC import ureal


class SQLDATA():
    def __init__(self, source):
        """

        Accesses the sqlite database created by caplogger on the windows 7 PC using the
        HP34970 as a switching resistance meter.
        Output is ultimately .jpg and .pdf files in \LoggerData\temperature_figs
        :param source:  string file name as in '\LoggerData\name.db'
        """
        self.t = INTERTIME('Pacific/Auckland')  # could be a parameter, but only used here
        self.source = source  # note that the source could be entered at the get_info method instead of the class
        self.wd = os.getcwd()  # get working directory

    def ohm_to_deg(self, r):
        """

        Same simple function as used in logging programme. Only useful for monitoring change.
        :param r: thermometer in ohm
        :return: temperature in degrees celsius
        """
        alpha = 0.00385  # for quick conversion to temperature
        temp = (r - 100.0) / (100.0 * alpha)
        return temp

    def temp_from_resist(self, R, R0=100.0):
        """
        formula for a PT-385, maybe better than ohm_to_deg
        :param R:
        :param R0:
        :return:
        """
        A = 3.9083e-3
        B = -5.775e-7
        ratio = R / R0
        discriminant = A ** 2 - 4 * B * (1 - ratio)
        if discriminant < 0:
            raise ValueError("Invalid resistance value: discriminant < 0")
        T = (-A + np.sqrt(discriminant)) / (2 * B)
        return T

    def get_info(self, begin, end):
        """

        :param begin: naive string datetime, assumed local time
        :param end: naive string datetime, assumed local time
        :return: dictionary {'Table name': result_dict} of result dictionaries {'dat_range':, 'time':, 'mean_time':,
         'temp':, 'mean_temp':, 'sd_temp':}
        """
        self.begin = begin  # bad way to make available to the plot!
        self.end = end
        start_string = begin
        finish_string = end
        selected_db = self.source
        # wd = os.getcwd()  # get working directory
        db_path = os.path.join(self.wd, selected_db)
        file_exists = os.path.exists(db_path)  # check it exists to avoid creating a blank
        if file_exists:
            conn = sqlite3.connect(selected_db)  # note the risk it will create one if it can't be found
            cursor = conn.cursor()
            sql_cmd = "SELECT name FROM sqlite_master WHERE type = 'table'"  # ORDER BY name"
            cursor.execute(sql_cmd)
            tables = cursor.fetchall()
            start = self.t.date_to_sec(start_string)
            finish = self.t.date_to_sec(finish_string)
            # set up dictionaries
            ref, sball, ref_temp, ah1, gr_in, gr_out, perm = {}, {}, {}, {}, {}, {}, {}
            table_dict = {'Reference': ref, 'S_ball': sball, 'Cropico_temp': ref_temp, 'AH11': ah1, 'GR_inner':gr_in,
                          'GR_outer': gr_out, 'Permutable': perm}

            for table in tables:
                if table[0] != 'Pressure':  # pressure is no longer being recorded in this system
                    sql = "SELECT time, value FROM " + table[0] + " WHERE time BETWEEN " + repr(start) + " AND " + repr(
                        finish)
                    cursor.execute(sql)
                    rowset = cursor.fetchall()
                    cx = []
                    cy = []
                    for row in rowset:
                        a = self.t.sec_to_date(row[0])  # epoch time to datetime
                        a = self.t.datetime_to_decimal_year(a)  # datetime to decimal year
                        cx.append(a)  # decimal year for plotting
                        cy.append(self.temp_from_resist(row[1]))  # simple temperature for plotting
                    mean_time = np.mean(cx)
                    mean_temp = np.mean(cy)
                    stdev_temp = np.std(cy)
                    table_dict[table[0]]['dat_range'] = (start_string, finish_string)
                    table_dict[table[0]]['time'] = cx
                    table_dict[table[0]]['temp'] = cy
                    table_dict[table[0]]['mean_time'] = mean_time
                    table_dict[table[0]]['mean_temp'] = mean_temp
                    table_dict[table[0]]['sd_temp'] = stdev_temp
                    # convenience for pasting data
                    print(table)
                    print(self.t.decimal_year_to_datetime(mean_time))
                    print(mean_time)
                    print(mean_temp)
                    print(stdev_temp)
                    print()

        else:
            print('File error in SQLDATA, probably misnamed')
            table_dict = {}  # empty dictionary
        return table_dict

    def plot_temp(self, input_dict, table):
        """

        plots temperature for one of the tables
        :param input_dict: from self.get_info
        :param table: name from 'Reference', 'S_ball', 'Cropico_temp', 'AH11', 'GR_inner',
                          'GR_outer', 'Permutable'.
        :return:
        """
        x_axis = input_dict[table]['time']
        y_axis = input_dict[table]['temp']
        print('x', x_axis)
        print('y', y_axis)
        plt.plot(x_axis, y_axis)
        plt.show()
        plt.close()

    def plot_all(self, input_dict):
        """

        plot all tables as a convenient
        :param input_dict: from self.get_info
        :return: stores jpg and pdf images of the graphs including temperatures in the legends
        """

        fig = plt.figure()
        f1 = fig.add_subplot(3, 2, 1)
        title = self.begin + ' - to - ' + self.end
        file_title = []
        for c in title:
            if c == ':':  # avoid colon in file name
                file_title.append('.')
            else:
                file_title.append(c)
        file_title = ''.join(file_title)  # this converts it into a string
        fig.suptitle(title)
        x1_axis = input_dict['Reference']['time']
        y1_axis = input_dict['Reference']['temp']
        temp1 = ureal(input_dict['Reference']['mean_temp'], input_dict['Reference']['sd_temp'])
        f1.plot(x1_axis, y1_axis, label='Reference' + str(temp1))
        plt.legend()
        f1.format_xdata = mdates.DateFormatter('%Y-%m-%d')

        f2 =fig.add_subplot(3, 2, 2)
        x2_axis = input_dict['GR_outer']['time']
        y2_axis = input_dict['GR_outer']['temp']
        temp2 = ureal(input_dict['GR_outer']['mean_temp'], input_dict['GR_outer']['sd_temp'])
        f2.plot(x2_axis, y2_axis, label='GR_outer' + str(temp2))
        x3_axis = input_dict['GR_inner']['time']
        y3_axis = input_dict['GR_inner']['temp']
        temp = ureal(input_dict['GR_inner']['mean_temp'], input_dict['GR_inner']['sd_temp'])
        f2.plot(x3_axis, y3_axis, label='GR_inner' + str(temp))
        plt.legend()

        f3 = fig.add_subplot(3, 2, 3)
        x4_axis = input_dict['Cropico_temp']['time']
        y4_axis = input_dict['Cropico_temp']['temp']
        temp = ureal(input_dict['Cropico_temp']['mean_temp'], input_dict['Cropico_temp']['sd_temp'])
        f3.plot(x4_axis, y4_axis, label='Cropico_temp' + str(temp))
        plt.legend()

        f4 = fig.add_subplot(3, 2, 4)
        x5_axis = input_dict['S_ball']['time']
        y5_axis = input_dict['S_ball']['temp']
        temp = ureal(input_dict['S_ball']['mean_temp'], input_dict['S_ball']['sd_temp'])
        f4.plot(x5_axis, y5_axis, label='S_ball' + str(temp))
        plt.legend()

        f5 = fig.add_subplot(3, 2, 5)
        x6_axis = input_dict['AH11']['time']
        y6_axis = input_dict['AH11']['temp']
        temp = ureal(input_dict['AH11']['mean_temp'], input_dict['AH11']['sd_temp'])
        f5.plot(x6_axis, y6_axis, label='AH11' + str(temp))
        plt.legend()

        f6 = fig.add_subplot(3, 2, 6)
        x7_axis = input_dict['Permutable']['time']
        y7_axis = input_dict['Permutable']['temp']
        temp = ureal(input_dict['Permutable']['mean_temp'], input_dict['Permutable']['sd_temp'])
        f6.plot(x7_axis, y7_axis, label='Permutable' + str(temp))
        plt.legend()

        fig.set_size_inches(11.69, 8.27)  # A4 landscape
        fig.autofmt_xdate()
        plt.tight_layout()
        fig_path = os.path.join(self.wd, 'LoggerData\\temperature_figs')
        plt.savefig(os.path.join(fig_path, file_title + '.pdf'))
        plt.savefig(os.path.join(fig_path, file_title + '.jpg'))
        plt.show()
        plt.close()


if __name__ == '__main__':
    # sql = SQLDATA('LoggerData\cap_environment_May_2022_on.db')
    # output_dict = sql.get_info('29 August, 2022, 1:30 PM', '30 August, 2022, 11:00 AM')  # with temperature blip
    # # output_dict = sql.get_info('29 August, 2023, 1:30 PM', '30 August, 2023, 11:00 AM')
    # # output_dict = sql.get_info('29 August, 2023, 1:30 PM', '30 August, 2024, 11:00 AM')
    # print(output_dict['Reference'])
    # print(output_dict['S_ball'])
    #
    # # output_dict = sql.get_info('29 August, 2022, 1:30 PM', '30 August, 2022, 11:00 AM')
    # # print(output_dict['Reference'])
    # # print(output_dict['S_ball'])
    # # sql.plot_temp(output_dict, 'S_ball')
    # sql.plot_all(output_dict)
    #
    # work through the historical data bases

    # date_tuples_1 = [('15 November, 2019, 9:00 AM', '15 November, 2019, 4:00 PM'),
    #                ('22 December, 2020, 9:00 AM', '22 December, 2020, 4:00 PM')]
    # sql = SQLDATA('LoggerData\cap_environment_August_2019_on.db')
    # for x in date_tuples_1:
    #     output_dict = sql.get_info(x[0], x[1])
    #     sql.plot_all(output_dict)


    # date_tuples_2 = [('3 September, 2021, 9:00 AM', '3 September, 2021, 4:00 PM'),
    #                ('9 September, 2021, 9:00 AM', '9 September, 2021, 4:00 PM'),
    #                ('9 September, 2021, 9:00 AM', '9 September, 2021, 4:00 PM'),
    #                ('10 September, 2021, 9:00 AM', '10 September, 2021, 4:00 PM'),
    #                ('21 September, 2021, 9:00 AM', '21 September, 2021, 4:00 PM'),
    #                ('11 October, 2021, 9:00 AM', '11 October, 2021, 4:00 PM')]
    # date_tuples_2 = [('12 April, 2022, 9:00 AM', '12 April, 2022, 4:00 PM')]
    date_tuples_2 = [('19 September, 2019, 9:00 AM', '19 September, 2019, 4:00 PM')]
    # date_tuples_2 = [('4 October, 2019, 9:00 AM', '4 October, 2019, 4:00 PM')]
    # sql = SQLDATA('LoggerData\cap_environment_September_2021_on.db')
    sql = SQLDATA('LoggerData\cap_environment_August_2019_on.db')
    for x in date_tuples_2:
        output_dict = sql.get_info(x[0], x[1])
        sql.plot_all(output_dict)

    # date_tuples_3 = [('3 July, 2025, 9:00 AM', '3 July, 2025, 4:00 PM'),
    #                ('4 July, 2025, 9:00 AM', '4 July, 2025, 4:00 PM'),
    #                ('7 July, 2025, 9:00 AM', '7 July, 2025, 4:00 PM'),
    #                ('8 July, 2025, 9:00 AM', '8 July, 2025, 4:00 PM')]
    # sql = SQLDATA('LoggerData\cap_environment_May_2022_on.db')
    # for x in date_tuples_3:
    #     output_dict = sql.get_info(x[0], x[1])
    #     sql.plot_all(output_dict)

    # date_tuples_4 = [('11 July, 2025, 9:00 AM', '11 July, 2025, 4:00 PM'),
    #                  ('23 October, 2025, 9:00 AM', '23 October, 2025, 4:00 PM'),
    #                  ('28 October, 2025, 9:00 AM', '28 October, 2025, 4:00 PM'),
    #                  ('3 November, 2025, 9:00 AM', '3 November, 2025, 4:00 PM'),
    #                  ('6 November, 2025, 9:00 AM', '6 November, 2025, 4:00 PM'),
    #                  ('21 November, 2025, 9:00 AM', '21 November, 2025, 4:00 PM'),
    #                  ('1 December, 2025, 9:00 AM', '1 December, 2025, 4:00 PM'),
    #                  ('5 December, 2025, 9:00 AM', '5 December, 2025, 4:00 PM')
    #                  ]
    # sql = SQLDATA('LoggerData\cap_environment_May_2022_05_Dec_2025.db')
    # for x in date_tuples_4:
    #     output_dict = sql.get_info(x[0], x[1])
    #     sql.plot_all(output_dict)

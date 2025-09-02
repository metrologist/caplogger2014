from sql_cap import SQLDATA
# need to pick up measurement data relevant to a set of capacitance measurements
# ideally made available as local time and temperature for easy matching
# Note that this is triggering some sort of recursive call on pyplot.....!!! avoid for now

print('select')
data = SQLDATA('LoggerData\cap_environment_May_2022_on.db')
output_dict = data.get_info('29 August, 2022, 1:30 PM', '30 August, 2022, 11:00 AM')
print(output_dict['Reference'])
print(output_dict['S_ball'])
data.plot_temp(output_dict, 'S_ball')
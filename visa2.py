"""
A simple class to allow quick testing of GPIB programs without instruments.
"""

import stuff

VisaIOError = False

def get_instruments_list():
	#specific to this setup
	return ['GPIB0::10', 'GPIB0::16']
	

class GpibInstrument(object):
	def __init__(self, name):
		self.name = name
		self.data = stuff.DataGen()
		
	def write(self, command):
		return
		
	def read_values(self):
		return [self.data.next()]
		


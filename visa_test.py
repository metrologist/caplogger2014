import visa
from time import sleep


logger = visa.GpibInstrument('GPIB::9')
logger.write("*IDN?")
a = logger.read()
print a
#logger.write("ERROR?")
#b = logger.read()
#print b
#logger.write("*RST")
#sleep(2)
logger.write("*CLS")
logger.write("DISP:TEXT 'MYVISA'") # front panel display
#logger.write("*RST")

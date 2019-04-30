import serial
import time
import pylab
import crc8
import numpy
import scipy
import MIT
import visa
import matplotlib.pyplot as plt
import read_the_temperature as rT
import single_chip_setup as scs
import accessory as acc
import calculation as clc
import write_bits as wb
from scipy import interpolate

def init_strat_work():
	rm = visa.ResourceManager()
	lst = rm.list_resources('?*')
	print(lst)
	my_instrument = rm.open_resource(lst[1])
	print(my_instrument)
	
	my_instrument.write("HEAD 1")
	#my_instrument.write("FLOW 0")
	time.sleep(5)
	my_instrument.write("HEAD 0")
	#my_instrument.write("FLOW 1")
	pass
	
def work(iterator):
	rm = visa.ResourceManager()
	lst = rm.list_resources('?*')
	my_instrument = rm.open_resource(lst[0])
	array_temperature = acc.get_the_array_of_temperature()
	if array_temperature[iterator]<20:
		my_instrument.write('SETN 2')
	elif array_temperature[iterator]<30:
		my_instrument.write('SETN 1')
	else:
		my_instrument.write('SETN 1')
	time.sleep(5)
	commands = "SETP " + str(array_temperature[iterator])
	my_instrument.write(commands)
	time.sleep(5)
	pass
	
def end_work():
	rm = visa.ResourceManager()
	lst = rm.list_resources('?*')
	my_instrument = rm.open_resource(lst[0])
	my_instrument.write("FLOW 0")
	time.sleep(5)
	my_instrument.write("HEAD 0")
	pass
	
init_strat_work()
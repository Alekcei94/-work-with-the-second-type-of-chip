import serial
import time
import pylab
import crc8
import numpy
import scipy
import MIT
import matplotlib.pyplot as plt
import read_the_temperature as rT
import single_chip_setup as scs
import accessory as acc
import calculation as clc
import write_bits as wb
from scipy import interpolate


'''
get temperature with MIT8
transfer ['2:1.32012E+01B '] -> 13.20
'''	
def get_temperature_with_mit(lineBinary):
	number_full_name = str(lineBinary).split(':')
	number_all = number_full_name[1].split('B')
	number = number_all[0].split('E+')
	temperature = float(number[0]) * (10**int(number[1]))
	print(number_full_name[0] + " Temperature = " + str(round(temperature, 2)))
	return round(temperature, 2)

'''
main function work MIT8
'''
def main_function_MIT(number_COM_port_MIT, start_pin, finish_pin):
	ser = serial.Serial('COM' + str(number_COM_port_MIT), 9600, timeout=0)
	ser.close()
	ser.open()
	ser.isOpen()
	flag = False
	size_array = finish_pin - start_pin + 1
	main_temperature = []
	for i in range(size_array):
		main_temperature.append(0)
	array_temperature = []
	start = start_pin
	while True:	
		lineBinary = ser.readlines()
		print(lineBinary)
		time.sleep(2)
		if len(str(lineBinary))<22 and len(str(lineBinary))>15 and 'E+' in str(lineBinary) and 'B ' in str(lineBinary):	
			if (str(start_pin) + ':') in str(lineBinary) and flag == False:
				print("start read MIT")
				flag = True
			if flag == True:
				#print(start)
				if (str(start) + ':') in str(lineBinary):
					array_temperature.append(get_temperature_with_mit(lineBinary))
					start = start +  1
					if (start > finish_pin):
						start = start_pin
						if check_MIT(main_temperature, array_temperature, size_array) == True:
							print("Finish point")
							break
						else:
							time.sleep(50)
							main_temperature = form_main_array(main_temperature, array_temperature, size_array)
							array_temperature = []
	return array_temperature

def form_main_array(main_temperature, array_temperature, size):
	iterator = 0
	flag = True
	for i in range(size):
		main_temperature[i] = array_temperature[i]
	return main_temperature
	
def check_MIT(main_temperature, array_temperature, size):
	iterator = 0
	flag = True
	for i in range(size):
		if main_temperature[i] != array_temperature[i]:
			flag = False
			break
	return flag
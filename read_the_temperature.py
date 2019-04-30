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
Read the temperature all schemes in file (-60 2048 0000111010101101)
'''
def read_the_temperature_all_schemes(ser):
	temperatura = input()
	lineBinary = scs.read_all_temperature(ser)
	if len(lineBinary) != 32:
		print ("What the chip not works!!!")
		pass
	plata = 1
	sxema = 1
	pin = [22,23,38,39]
	j=0
	i=1 
	for elem in lineBinary:
		if sxema >8:
			plata=plata+1
			sxema=1
			#j=j+1
		numberElment = 0
		number = ""
		for bit in elem:	
			if (numberElment>=4) and (numberElment<16):
				number = number + str(bit)
			numberElment = numberElment + 1
		fileText = open('../../data/'+str(pin[j])+'.txt', 'a')
		fileText.write(str(temperatura) + " " + str(int(number,2)) + " " + str(elem))
		fileText.close()
		pin[j]=pin[j]+1
		i=i+1
	pass
	
	
'''
Test method (-60 2048 0000111010101101)
'''
def write_in_file_the_temperature_all_schemes_test(ser, MIT_COM_port, MIT_start_port, MIT_finish_port, flag_use_MIT):

	if flag_use_MIT == True:
		array_temperature = []
		array_temperature = MIT.main_function_MIT(MIT_COM_port, MIT_start_port, MIT_finish_port)
		if len(array_temperature)<8:
			size = len(array_temperature)
			for i in range(size,8):
				array_temperature.append(-1000)
		lineBinary = scs.read_all_temperature(ser)
		array_average_temperature = form_array_average_temperature(array_temperature)
		iterator = 0
		temperatura = 999
		for elem in lineBinary:
			real_temperature_12_bit = ""
			list_elem = list(elem)
			for i in range(4, len(elem)):
				real_temperature_12_bit += str(list_elem[i])
			print("TEST = " + real_temperature_12_bit)
			port = iterator + 22
			print(iterator)
			if acc.get_1_pin(port) == True:
				temperatura = array_average_temperature[0]
			elif acc.get_2_pin(port) == True:
				temperatura = array_average_temperature[1]
			elif acc.get_3_pin (port) == True:
				temperatura = array_average_temperature[2]
			elif acc.get_4_pin (port) == True:
				temperatura = array_average_temperature[3]
			else:
				print("!!!!")
			iterator = iterator + 1
			fileText = open('../../data/'+str(port)+'.txt', 'a')
			fileText.write(str(temperatura) + " " + str(int(real_temperature_12_bit,2)) + " " + str(elem))
			fileText.close()
	else:
		lineBinary = scs.read_all_temperature(ser)
		iterator = 0
		print("Write temperature:")
		temperatura = input()
		print(lineBinary)
		for elem in lineBinary:
			real_temperature_12_bit = ""
			list_elem = list(elem)
			for i in range(4, len(elem)):
				real_temperature_12_bit += str(list_elem[i])
			port = iterator + 22
			iterator = iterator + 1
			fileText = open('../../data/'+str(port)+'.txt', 'a')
			fileText.write(str(temperatura) + " " + str(int(real_temperature_12_bit,2)) + " " + str(elem))
			fileText.close()
	pass

	
'''
Create an array of average temperature with MIT sensors.
'''	
def form_array_average_temperature(array_temperature):
	array_average_temperature = []
	i = 0
	while True:
		if i<len(array_temperature):
			average_temperature = (array_temperature[i] + array_temperature[i+1])/2
			array_average_temperature.append(round(average_temperature, 2))
			i = i + 2
		else:
			break
	return array_average_temperature
	
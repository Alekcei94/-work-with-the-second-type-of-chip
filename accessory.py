import datetime
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
import test_ADDRESS as tADR
from scipy import interpolate

'''
Form name file. This name -> 22.02.2019
'''
def set_data_log():
	today = datetime.datetime.now()
	data = str(today.day) + '_' + str(today.month) + '_' + str(today.year)
	return data

'''
write log
'''
def write_log(pin_arduino, text):
	file = open('../../log/log_work_' + set_data_log() + '.log', 'a')
	file.write(str(pin_arduino) + " --  " + text + '\n')
	file.close()		
	pass

'''
Past pause
'''	
def pause():
	print("Continue" + "\n" + "1 - yes")
	set = input()
	pass

'''
Past pause in hight voltage
'''
def pause_time_read_temperature():
	print("--- Read temperature? ---" + "\n" + "1 - yes")
	set = input()
	pass

'''
Read all file and forming a file with all the data.
'''
def writeFileAllInOneFile():
	list = []
	for i in range(get_start_arduino_port(), get_finish_arduino_port()+1):
		c, b = clc.readFile(str(i))
		list.append(b)
	fileText = open('../../data/All.txt', 'w')
	#KOD = list[0]
	k=0
	for i in range(get_start_arduino_port(), get_finish_arduino_port()+1):
		fileText.write(" " + str(i) + " |  ")
		KOD = list[k]
		print(KOD)
		k=k+1
		j=0
		while True:
			if (j>=len(KOD)):
				fileText.write('\n')
				break
			fileText.write(str(KOD[j]) + " |  ")
			j=j+1
	fileText.close()
	pass
	
'''
This method is needed to find the board used.
'''
def get_1_pin(pin):
	array = [22,24,26,28,30,32,34,36]
	flag = False
	for i in array:
		if pin == i:
			flag = True
			break
	return flag
	
'''
This method is needed to find the board used.
'''
def get_3_pin(pin):
	array = [38,40,42,44,46,48,50,52]
	flag = False
	for i in array:
		if pin == i:
			flag = True
			break
	return flag
	
'''
This method is needed to find the board used.
'''
def get_2_pin(pin):
	array = [23,25,27,29,31,33,35,37]
	flag = False
	for i in array:
		if pin == i:
			flag = True
			break
	return flag

'''
This method is needed to find the board used.
'''
def get_4_pin(pin):
	array = [39,41,43,45,47,49,51,53]
	flag = False
	for i in array:
		if pin == i:
			flag = True
			break
	return flag
	
'''
Form and get ideal coefficient K and B
'''
def get_ideal_k_and_b():
	'''
	x - Temperature;
	y - KOD;
	'''
	x_1 = -60
	y_1 = 3280
	#y_1 = 3007
	x_2 = 125
	y_2 = 784
	#y_2 = 47
	k = float((y_1-y_2))/float((x_1-x_2))
	b = y_2 - k*x_2
	return k, b

'''
get the number of passable points to remove temperatures
'''
def get_the_number_of_points():
	number_of_points = int(8)
	return number_of_points

'''
get the the array of temperature
'''
def get_the_array_of_temperature():
	array_temperature = [-62, -32, -7, 20, 42, 62, 92, 126]
	return array_temperature
	
'''
get start arduino port
'''	
def get_start_arduino_port():
	start_arduino_port = int(22)
	return start_arduino_port

'''
get finish arduino port
'''	
def get_finish_arduino_port():
	finish_arduino_port = int(22)
	return finish_arduino_port

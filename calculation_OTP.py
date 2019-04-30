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
Test function
'''
def calculation_ADDRESS_and_KOD_test(ser, port):
	iterator = 0
	while iterator<=255:
		y_ADDRESS = 255
		y_KOD = 3007
		print(str(y_ADDRESS) + " __ " + str(int(y_KOD)))
		wb.write_OTP(ser, int(y_ADDRESS), int(y_KOD), port)
		#iterator+=1
		break
	pass

'''
calculation address and KOD in chip (256 byte)
'''	
def calculation_ADDRESS_and_KOD(ser):
	x_list_in_file = []
	y_list_in_file = []
	port_arduino = 22
	port = tADR.give_number_port(ser)
	x_list_in_file, y_list_in_file = clc.readFile(str(port))
	all_x_in_interpol, all_y_in_interpol = clc.interpol(x_list_in_file, y_list_in_file)
	# not TRUE
	k, b = clc.get_k_and_b(x_list_in_file, y_list_in_file)
	k_line_KOD = -16
	b_line_KOD = 2047
	delta_K_line = round(float(k_line_KOD/k), 4)
	delta_B_line = int(-1*((k_line_KOD/k) * b) + b_line_KOD)	
	k_ideal, b_ideal = acc.get_ideal_k_and_b()
	k_real = round(float(k_ideal/k), 4)
	b_real = -1*((k_ideal/k)*b)+b_ideal
	iterator = 0
	KOD = []
	ADDRESS = []
	KOD, ADDRESS = form_array_in_read_file(all_x_in_interpol, all_y_in_interpol, x_list_in_file, y_list_in_file, k_real, b_real, k_line_KOD, b_line_KOD)
	KOD, ADDRESS = check_formed_array(KOD, ADDRESS)
	KOD, ADDRESS = check_formed_array_2(KOD, ADDRESS)
	iterator_array_KOD_AND_ADDRESS = 0
	start_address = wb.form_array_full_address_start_or_finish(ADDRESS[0])
	finish_address =  wb.form_array_full_address_start_or_finish(ADDRESS[-1])
	print(str(start_address) + " !!!__!!! " + str(finish_address))
	while iterator<=255:
		#print(" Write address in " + str(iterator) + " line")
		if iterator==0:
			y_ADDRESS = 0
			y_KOD = 47
			print(str(wb.form_array_full_address_start_or_finish(y_ADDRESS)) + " __ " + str(int(y_KOD)))
			wb.write_OTP(ser, int(y_ADDRESS), int(y_KOD), port_arduino)
		elif iterator<start_address:
			y_ADDRESS = iterator
			y_KOD = 47
			print(str(wb.form_array_full_address_start_or_finish(y_ADDRESS)) + " __ " + str(int(y_KOD)))
			wb.write_OTP(ser, int(y_ADDRESS), int(y_KOD), port_arduino)
		elif iterator>finish_address:
			y_ADDRESS = iterator
			y_KOD = 3007
			print(str(wb.form_array_full_address_start_or_finish(y_ADDRESS)) + " __ " + str(int(y_KOD)))
			wb.write_OTP(ser, int(y_ADDRESS), int(y_KOD), port_arduino)
		else:
			y_ADDRESS = ADDRESS[iterator_array_KOD_AND_ADDRESS]
			y_KOD = KOD[iterator_array_KOD_AND_ADDRESS]
			print(str(wb.form_array_full_address_start_or_finish(y_ADDRESS)) +  " __ " + str(int(y_KOD)))
			wb.write_OTP(ser, int(y_ADDRESS), int(y_KOD), port_arduino)
			iterator_array_KOD_AND_ADDRESS = iterator_array_KOD_AND_ADDRESS + 1
		iterator+=1
	pass


def form_array_in_read_file(x_list_interpol, y_list_interpol, x_list_in_file, y_list_in_file, k_real, b_real, k, b):
	KOD_array = []
	ADDRESS_array = []
	size = len(x_list_in_file)
	for i in range(size-1, 0, -1):
		#print(" start temperature = " + str(x_list_in_file[i]) + " finish temperature = " + str(x_list_in_file[i-1]))
		start_address = give_me_address_in_255(y_list_in_file[i], k_real, b_real)
		finish_address = give_me_address_in_255(y_list_in_file[i-1], k_real, b_real)
		print(" finish = " + str(finish_address) + " start = " + str(start_address))
		razn = int(finish_address) - int(start_address)
		step_temperature = abs(round(((abs(x_list_in_file[i]) - abs(x_list_in_file[i-1]))/razn),2))
		#print(" step temperature = " + str(step_temperature))
		temperature = x_list_in_file[i]
		KOD_ADDRESS = round(y_list_in_file[i],0)
		for j in range(razn):
			KOD = int(temperature * k + b)
			KOD_array.append(KOD)
			ADDRESS = int(KOD_ADDRESS * k_real + b_real)
			bin_address = str(bin(ADDRESS))
			test = bin_address[2:len(bin_address)-1]
			#print(str(bin_address) + " ___ " + str(int(test,2)))
			ADDRESS = int(test,2)
			#ADDRESS_array.append(give_me_address_in_25_test(ADDRESS))
			ADDRESS_array.append(ADDRESS)
			print(" KOD = " + str(KOD) + " ADDRESS = " + str(ADDRESS) + " temperature = " + str(temperature) + " step = " + str(step_temperature) + " KOD_ADDRESS = " + str(KOD_ADDRESS))
			temperature = round((temperature - step_temperature), 2)
			index_int = x_list_interpol.index(temperature)
			KOD_ADDRESS = round(y_list_interpol[index_int], 0)
	return KOD_array, ADDRESS_array

	
def give_me_address_in_255(KOD, k_test, b_test):
	address_12_bit = KOD * k_test + b_test
	print(address_12_bit)
	address_12_bit = str(bin(int(address_12_bit)))
	address_bit = list(address_12_bit[2:len(address_12_bit)])
	print(address_bit)
	if len(address_bit) > 8:
		#razn = len(address_bit) - 8
		for i in range(4):
			del address_bit[len(address_bit)-1]
	address_255 = ""
	for i in address_bit:
		address_255 += str(i)
	address = int(address_255, 2)
	return address

	
def check_formed_array(KOD, ADDRESS):
	iterator = 0
	while True:
		if iterator>len(KOD)-2:
			break
		top_address = wb.form_array_full_address_start_or_finish(ADDRESS[iterator])
		bottom_address = wb.form_array_full_address_start_or_finish(ADDRESS[iterator+1])
		#print(str(top_address) + " !!! " + str(bottom_address))
		if top_address == bottom_address:
			del KOD[iterator + 1]
			del ADDRESS[iterator + 1]
		iterator += 1
	return KOD, ADDRESS


def check_formed_array_2(KOD, ADDRESS):
	iterator = 0
	while True:
		if iterator>len(KOD)-2:
			break
		top_address = wb.form_array_full_address_start_or_finish(ADDRESS[iterator])
		bottom_address = wb.form_array_full_address_start_or_finish(ADDRESS[iterator+1])
		#print(str(top_address) + " !!! " + str(bottom_address))
		raznost = bottom_address - top_address
		if raznost > 1:
			step = (KOD[iterator+1]-KOD[iterator])/raznost
			new_KOD = KOD[iterator]
			new_ADDRESS = top_address
			for i in range(int(raznost) - 1):
				new_ADDRESS += 1
				new_KOD += step
				#print(str(new_ADDRESS) + " _#_ " + str(new_KOD))
				KOD.insert(iterator+1+i,int(new_KOD))
				ADDRESS.insert(iterator+1+i,new_ADDRESS)
		iterator += 1
	return KOD, ADDRESS
	
'''
Test function
'''	
def give_me_address_in_25_test(KOD):
	address_12_bit = str(bin(int(KOD)))
	address_bit = list(address_12_bit[2:len(address_12_bit)])
	if len(address_bit) > 8:
		#razn = len(address_bit) - 8
		for i in range(4):
			del address_bit[len(address_bit)-1]
	address_255 = ""
	for i in address_bit:
		address_255 += str(i)
	address = int(address_255, 2)
	return address
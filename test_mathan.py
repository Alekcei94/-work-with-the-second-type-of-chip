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
import calculation_OTP as clc_OTP
import one_Use as oU
from scipy import interpolate

def write_OTP( address, KOD, port):
	#print ("\n" + "BINARY BLOCK")
	bit_ADDRESS = str(bin(address))
	bit_ADDRESS = list(bit_ADDRESS[2:len(bit_ADDRESS)])
	print(bit_ADDRESS)
	if len(bit_ADDRESS) == 12:
		del bit_ADDRESS[11]
	print(bit_ADDRESS)
	bit_KOD = str(bin(KOD))
	bit_KOD = list(bit_KOD[2:len(bit_KOD)])
	bin_code = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	iterator = len(bit_ADDRESS)-1
	for bit in bit_ADDRESS:
		bin_code[iterator] = int(bit)
		iterator = iterator - 1
	iterator = len(bit_KOD)+10
	for bit in bit_KOD:
		bin_code[iterator] = int(bit)
		iterator = iterator - 1
	print(bin_code)
	byte = ""
	iterator = 0
	package = []
	for bit in bin_code:
		if iterator == 7:
			package.append(chr(int(byte,2)))
			#print(byte)
			byte = str(bit)
			iterator = 1
		else:
			byte += str(bit)
			iterator += 1
	#print(package)
	#ser.write('7')	
	number_p = chr(int(port) - 22)
	#ser.write(number_p)	
	#for i in package:
		#print(i)
		#ser.write(i)
	#time.sleep(2)
	#Yokogaws.fire()
	#time.sleep(2)
	#acc.pause()
	pass
	
def calculation_ADDRESS_and_KOD(port):
	x_list_in_file = []
	y_list_in_file = []
	x_list_in_file, y_list_in_file = clc.readFile(port)
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
	y = 16
	print(" k = " + str(k_real) + " b = " + str(b_real))
	clc_OTP.form_array_in_read_file(all_x_in_interpol, all_y_in_interpol, x_list_in_file, y_list_in_file, k_real, b_real, k_line_KOD, b_line_KOD)
	#clc_OTP.give_me_address_in_255(int(-10), k_real, b_real)
	'''
	iterator = 0
	while iterator<=255:
		print(" Write address in " + str(iterator) + " line")
		if iterator==0:
			y_ADDRESS = 4080
			y_KOD = 47
			print(str(y_ADDRESS) + " __ " + str(round(y_KOD,0)))
			time.sleep(4)
			write_OTP(int(y_ADDRESS), int(y_KOD), port)
		elif iterator<50:
			y_ADDRESS = 0
			y_KOD = 47
			print(str(y_ADDRESS) + " __ " + str(round(y_KOD,0)))
			#wb.write_OTP(ser, int(y_ADDRESS), int(y_KOD), port)
		elif iterator>205:
			y_ADDRESS = 0
			y_KOD = 3007
			print(str(y_ADDRESS) + " __ " + str(round(y_KOD,0)))
			#wb.write_OTP(ser, int(y_ADDRESS), int(y_KOD), port)
		else:
			x = (((y-b_real)/k_real)-b)/k
			y_ADDRESS = (x*k+b)*k_real+b_real
			y_KOD = (x*k+b)*delta_K_line+delta_B_line
			print(str(y_ADDRESS) + " __ " + str(round(y_KOD,0)))
			#wb.write_OTP(ser, int(y_ADDRESS), int(y_KOD), port)
		iterator+=1
		y = y+8
	'''
	pass

	
def graph(xlist_0, ylist_0, xlist_1, ylist_1):
	plt.axis([-70, 135, 0, 4300])
	plt.plot(xlist_0, ylist_0, color = 'red')
	plt.plot(xlist_1, ylist_0, color = 'blue')
	plt.show()
	pass

'''
main coefficient calculation method
'''	
def calculation_coefficients(g):
	#enter the file number
	numberPin = int(g)
	x_list_in_file = []
	y_list_in_file = []
	x_list_in_file, y_list_in_file = readFile(g)
	all_x_in_interpol, all_y_in_interpol = interpol(x_list_in_file, y_list_in_file)
	k,b = get_k_and_b(x_list_in_file, y_list_in_file)
	k_ideal, b_ideal = acc.get_ideal_k_and_b()
	k_real = round(float(k_ideal/k), 4)
	b_real = round((-1*((k_ideal/k)*b)+b_ideal),0)
	print("k = " + str(k_real) + " b = " + str(b_real))
	clc_OTP.give_me_address_in_255(2765 , k_real, b_real)
	pass

def get_k_and_b(x_list_in_file, y_list_in_file):
	x_1 = x_list_in_file[0]
	y_1 = y_list_in_file[0]
	x_2 = x_list_in_file[-1]
	y_2 = y_list_in_file[-1]
	k = float((y_1-y_2))/float((x_1-x_2))
	b = y_2 - k*x_2
	return k, b

'''
least squares optimization method
'''	
def min_kv(x_list_interval, y_list_interval):
	summa_x = 0
	kv_summ_x = 0
	summa_y = 0
	summ_x_y_proizv = 0
	for i in range(len(x_list_interval)):
		summa_x = summa_x + x_list_interval[i]
		kv_summ_x = kv_summ_x + (x_list_interval[i]*x_list_interval[i])
		summa_y = summa_y + y_list_interval[i]
		summ_x_y_proizv = summ_x_y_proizv + (x_list_interval[i]*y_list_interval[i])
	delta = (kv_summ_x * len(x_list_interval)) - (summa_x * summa_x)
	delta_k = (summ_x_y_proizv*len(x_list_interval)) - (summa_y*summa_x)
	delta_b = (kv_summ_x*summa_y) - (summ_x_y_proizv*summa_x)

	coef_k = float(delta_k/delta)
	coef_b = float(delta_b/delta)
	
	return coef_k, coef_b

'''
get cubic interpolation coordinates [KOD temperature]
'''	
def interpol(xlist_test, ylist_test):
	tck = interpolate.splrep(xlist_test, ylist_test)
	temperaturerite = xlist_test[0]
	stop_step = xlist_test[len(xlist_test)-1]
	step = 0.01
	interval_y = []
	interval_x = []
	interval = []
	while temperaturerite < stop_step:
		interval_x.append(temperaturerite)
		interval_y.append(interpolate.splev(temperaturerite, tck))
		temperaturerite = temperaturerite + step
	return interval_x, interval_y

'''
read file and get KOD temperature
'''
def readFile(i):
	try: 
		file = open('../../data/'+ i +'.txt', 'r')
		say = []
		kod_list = []
		T_list = []
		for line in file:
			say = line.split(' ')
			if len(say)>0:
				kod_list.append(float(say[0]))
				T_list.append(float(say[1]))
		file.close()
		return kod_list, T_list
	except:
		pass

'''
1925
1914

1936
2144
pogreshnost coef k and b
'''	
def pogreshnost_coef_k_and_b(k, b, k_1, b_1, x_list):
	iterator = 0
	sum_razn = 0
	for x in x_list:
		new_y = (x*k_1+b_1)*k+b
		k1, b1 = acc.get_ideal_k_and_b()
		y = x*k1 + b1
		razn = new_y - y
		sum_razn = sum_razn + razn
		iterator+=1
	return (sum_razn/iterator)
	
	

flag=True
col_list = []
#calculation_coefficients("28")
#calculation_ADDRESS_and_KOD("22")
Yokogaws.fire_9V()
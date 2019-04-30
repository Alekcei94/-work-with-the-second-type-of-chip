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
from scipy import interpolate


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
build graph
'''		
def build_graph(xlist_test1, ylist_test1):
	plt.axis([-70, 135, -10000, 10000])
	plt.plot(xlist_test1, ylist_test1, color = 'red')
	plt.plot([-60, 125], [4095, 15], color = 'blue')
	plt.show()
	pass

'''
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
		print(" new_y = " + str(int(new_y)) + " y = " + str(int(y)))
		sum_razn = sum_razn + razn
		iterator+=1
	return (sum_razn/iterator)
	
'''
Test function
'''	
def test_version(x_list):
	x_1 = 125
	y_1 = 47
	x_2 = -55
	y_2 = 2927
	k = float((y_1-y_2))/float((x_1-x_2))
	b = y_2 - k*x_2
	y_list = []
	for x in x_list:
		y_list.append(x*k+b)
		print(str(x) + " __ y __ " + str(x*k+b))
	build_graph(x_list, y_list)
	pass
	
def test_1():
	i = 2040
	step = 8
	while True:
		if i<=8:
			break
		else:
			print (chr(hex(i)))
			i = i - step
	pass
	
'''
main coefficient calculation method
'''	
x_list_in_file = []
y_list_in_file = []
x_list_in_file, y_list_in_file = readFile(str(24))
'''
all_x_in_interpol, all_y_in_interpol = interpol(x_list_in_file, y_list_in_file)
k,b = min_kv(all_x_in_interpol, all_y_in_interpol)
'''
all_x_in_interpol = []
for i in range(int(x_list_in_file[-1]-x_list_in_file[0])):
	all_x_in_interpol.append(i)
k,b = get_k_and_b(x_list_in_file, y_list_in_file)
print("k = " + str(k) + " b = " + str(b))
#new_y_list = []
k_ideal, b_ideal = acc.get_ideal_k_and_b()
k_real = round(float(k_ideal/k), 4)
b_real = int(-1*((k_ideal/k)*b)+b_ideal)
#k_real = 3.33
#b_real = -4850
print("k = " + str(k_real) + " b = " + str(b_real))
	
#print("file = " + g)
print(str(pogreshnost_coef_k_and_b(k_real, b_real, k, b, x_list_in_file)))
#test_version(all_x_in_interpol)
#clc_OTP.calculation_ADDRESS_and_KOD(ser, g, all_x_in_interpol)

#wb.write_coefficient(ser, k_real, b_real, numberPin)

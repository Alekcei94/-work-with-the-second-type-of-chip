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

def one_use_function(ser, port):
	arra_Address = [191, 310, 434, 573, 713]
	array_KOD = [185, 351, 507, 678, 835]
	iterator = 0
	y_ADDRESS = 88
	KOD = 47
	for i in range(len(arra_Address)):
		size = (arra_Address[iterator]-y_ADDRESS)//8
		step_KOD = (array_KOD[iterator]-KOD)//size
		for j in range(size):
			y_ADDRESS = y_ADDRESS + 8
			KOD = KOD + step_KOD
			print(" Address = " + str(y_ADDRESS) + " KOD = " + str(KOD))
			wb.write_OTP(ser, y_ADDRESS, KOD, port)
		iterator = iterator + 1
	pass
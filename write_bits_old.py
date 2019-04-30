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
Method of recording the coefficients of K and B in the chip
'''
def write_coefficient(ser, coefK, coefB, port):
	print("CoefK = " + str(coefK) + " coefB = " + str(coefB))
	print ("\n" + "BINARY BLOCK")
	#
	#block sending data
	#
	bin_Code_Coef_B = []
	binCodeCorfK = []
	#for ele in coefB:
	x = int(coefB)
	bin_Code_Ele_B=[0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	i=0
	if coefB<0:
		bin_Code_Ele_B[13] = 1
		x = x*(-1)
	else:
		bin_Code_Ele_B[13] = 0
	n = ""
	while x > 0:
		y = str(x % 2)
		if i<13:
			bin_Code_Ele_B[i] = int(y)
			i=i+1
		else:
			break
		x = int(x / 2)
	coef_b_text = ""
	for z in bin_Code_Ele_B:
		bin_Code_Coef_B.append(z)
		coef_b_text = coef_b_text + str(z)
	print ("b = " + coef_b_text)
	
	#for ele in coefK:
	x = float(coefK)
	binCodeEleK=[0,0,0,0,0,0,0,0,0,0,0,0,0]
	intX = int(x)
	i = 10
	while i < 13:
		y = str(intX % 2)
		binCodeEleK[i] = int(y)
		i=i+1
		intX = int(intX / 2)
	intY = float(coefK) - int(coefK)
	i=9
	while i>=0:
		z = intY * 2
		binCodeEleK[i] = int(z)
		intY = float(z) - int(z)
		i=i-1
	coefkk = ""
	for ele in binCodeEleK:
		coefkk = coefkk + str(ele)
		binCodeCorfK.append(ele)
	print ("k = " + coefkk)

	pacet = []
	for i in range(0, 13):
		pacet.append(binCodeCorfK[i])
	for i in range(0, 14):
		pacet.append(bin_Code_Coef_B[i])
	
	#enable 1
	pacet.append(1)
	for i in range(4):
		pacet.append(0)
	text = ""
	iterat = 0
	win_test = []
	for i in range(len(pacet)+1):
		if iterat < 8:
			text = text + str(pacet[i])
			iterat =iterat + 1
		else:
			not_Invers = list(text)
			nul = 7
			invers = ""
			for j in range(8):
				invers = invers + not_Invers[nul]
				nul-=1
			win_test.append(chr(int(invers,2)))
			test =  hex(int(invers,2))
			text = ""
			if i != 32:
				text = text + str(pacet[i])
			iterat =1
	print ("-------------------------" + "\n")
	
	ser.write('1')	
	number_p = chr(port - 22)
	ser.write(number_p)	
	for i in win_test:
		print(i)
		ser.write(i)
	print("Please wait 4 seconds. " + '\n')
	time.sleep(4)
	pass
	
'''
Method of recording the coefficients of K and B in the chip
'''
def write_OTP(ser, address, KOD, port):
	print ("\n" + "BINARY BLOCK")
	bit_ADDRESS = str(bin(address))
	bit_ADDRESS = list(bit_ADDRESS[2:len(bit_ADDRESS)])
	bit_KOD = str(bin(KOD))
	bit_KOD = list(bit_KOD[2:len(bit_KOD)])
	bin_code = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	iterator = 10
	for bit in bit_ADDRESS:
		bin_code[iterator] = int(bit)
		iterator = iterator - 1
	iterator = 22
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
			byte = str(bit)
			iterator = 1
		else:
			byte += str(bit)
			iterator += 1
	print(package)
	ser.write('7')	
	number_p = chr(int(port) - 22)
	ser.write(number_p)	
	for i in package:
		#print(i)
		ser.write(i)
	time.sleep(2)
	acc.pause()
	pass
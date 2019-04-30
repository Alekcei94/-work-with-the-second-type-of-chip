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
read temperature
'''
def read_all_temperature(ser):
	start_point = acc.get_start_arduino_port()
	finish_point = acc.get_finish_arduino_port()
	ser.write('6')
	time.sleep(3)
	'''
	while True:
		if start_point > finish_point:
			break
		else:
			#lines = ""
			ser.write('0')
			ser.write(start_point)
			#time.sleep(1)
			start_point = start_point + 1
			#lines = ser.readline()
			#print(lines)
	'''
	ser.write('0')
	time.sleep(6)
	all_lines = []
	all_lines = ser.readlines()
	lines = []
	#print(len(all_lines))
	for i in range(start_point - 22, finish_point + 1 - 22):
		#print(i)
		lines.append(all_lines[i])
	#print(lines)
	return lines

'''
Check for proper operation of the chip
'''
def circuit_health_check(ser, number_pin_arduino, lineBinary):
	pin = int(number_pin_arduino-22)
	list_check_rez = []
	list_check_rez = list(lineBinary[pin])
	list_check_rez.remove('\r')
	list_check_rez.remove('\n')
	print(" KOD = " + str(list_check_rez) + " PIN = " + str(number_pin_arduino))
	if len(list_check_rez)>0:
		if int(list_check_rez[5])==1 or int(list_check_rez[6])==1:
			flagWork = False
			acc.write_log(number_pin_arduino, "--Chip does not work--")
		else:
			flagWork = True
	else:
		flagWork = False
		acc.write_log(number_pin_arduino, "--No chip--")
	return flagWork
	
'''
Check the stitched REZ
ser - com port arduino
number_pin_arduino - number port arduino
'''
def check_REZ(ser, number_pin_arduino, lineBinary): 
	number_pin_arduino = int(number_pin_arduino-22)
	list_check_rez = []
	list_check_rez = list(lineBinary[number_pin_arduino])
	list_check_rez.remove('\r')
	list_check_rez.remove('\n')
	print(list_check_rez)
	if len(list_check_rez)>4:
		if int(list_check_rez[5])==1:
			flagWork = True
		else:
			flagWork = False
			acc.write_log(number_pin_arduino, "--Recording REZ went wrong--")
	else:
		flagWork = False
	return flagWork

'''
check address chip
'''
def check_address(ser, number_pin_arduino):
	ser.write('4')
	pin = chr(number_pin_arduino - 22)
	ser.write(pin)
	time.sleep(2)
	line = ser.readlines()
	result = int(line[0])
	if result == 1:
		flagWork = True
		print ("crc8 - true")
	elif result ==0:
		flagWork = False
		print("crc8 - false")
	full_address = "\n" + " "
	for i in range(1,9):
		full_address = full_address + line[i] + " "
	print ("Full address = " + full_address)
	return flagWork

'''
set REZ
'''
def set_REZ(ser, pin_array):
	ser.write('6')
	time.sleep(3)
	for pin in pin_array:
		ser.write('2')
		ser.write(pin)
	time.sleep(2)
	"""
	source job!!
	"""
	print ("Continue _ sleep Set_REZ ")
	str(input())
	pass

'''
set Address
number_family - 1:BMK_GEN (0x28); 2:BMK_DIODS (0x29); 3:CUSTOM_GEN (0x06); 4:CUSTOM_DIODS (0x07); 5:TEST_SAMPLE (0xAD);
type_of_party - 0010; 0000; 0011;
'''
def set_address(ser, number_family, type_of_party, pin_arduino):
	number_family = int(number_family)
	crc1 = ""
	#bin_name = -1
	pin = pin_arduino-22
	print(type_of_party)
	type_of_party = str(type_of_party)
	print(type_of_party)
	if number_family == 1:
		bin_name = form_ADDRESS_SN(ser,0)
		crc1 = write_CRC(ser, 0, pin, type_of_party)
		fileText = open('../../listing_address/BMK_GEN.list', 'a')
		fileText.write("40" + " " + str(type_of_party) + " " + str(bin_name) + " " + str(crc1) + "\n")
		print ("-------------------------" + "\n")
		fileText.close()
	elif number_family == 2:
		bin_name = form_ADDRESS_SN(ser,1)
		crc1 = write_CRC(ser, 1, pin, type_of_party)
		fileText = open('../../listing_address/BMK_DIODS.list', 'a')
		fileText.write("41" + " " + type_of_party + " " + str(bin_name) + " " + str(crc1) + "\n")
		print ("-------------------------" + "\n")
		fileText.close()
	elif number_family == 3:
		bin_name = form_ADDRESS_SN(ser,2)
		crc1 = write_CRC(ser, 2, pin, type_of_party)
		fileText = open('../../listing_address/CUSTOM_GEN.list', 'a')
		fileText.write("6" + " " + type_of_party + " " + str(bin_name) + " " + str(crc1) + "\n")
		print ("-------------------------" + "\n")
		fileText.close()
	elif number_family == 4:
		bin_name = form_ADDRESS_SN(ser,3)
		crc1 = write_CRC(ser, 3, pin, type_of_party)
		fileText = open('../../listing_address/CUSTOM_DIODS.list', 'a')
		fileText.write("7" + " " + type_of_party + " " + str(bin_name) + " " + str(crc1) + "\n")
		print ("-------------------------" + "\n")
		fileText.close()
	elif number_family == 5:
		bin_name = form_ADDRESS_SN(ser,4)
		crc1 = write_CRC(ser, 4, pin, type_of_party)
		fileText = open('../../listing_address/TEST_SAMPLE.list', 'a')
		fileText.write("173" + " " + type_of_party + " " + str(bin_name) + " " + str(crc1) + "\n")
		print ("-------------------------" + "\n")
		fileText.close()
	elif number_family == 6:
		return
	else:
		print ("incorrect value entered")
		write_adres(ser, pin)
	pass

'''
Write in file full address
'''
def form_ADDRESS_SN(ser, number_file):
	bin_name = 0
	address = []
	name_file = ["BMK_GEN","BMK_DIODS","CUSTOM_GEN","CUSTOM_DIODS","TEST_SAMPLE"]
	fileText = open('../../listing_address/'+name_file[number_file]+'.list', 'r')
	all_lines = fileText.readlines()
	fileText.close()
	if len(all_lines) == 0:
		return bin_name
	else:
		last_line = all_lines[-1].split(" ")
		bin_name = int(last_line[2])+1
	return bin_name

'''
form CRC8 and write full address in chip
'''
def write_CRC(ser, number_file, pin, type_of_party):
	crc = [0,0,0,0,0,0,0,0]
	ishod = ""
	code = []
	FAM = []
	SN = []
	PARTY = []
	print(type_of_party)
	for i in range(56):
		code.append(0)
	name_file = ["BMK_GEN","BMK_DIODS","CUSTOM_GEN","CUSTOM_DIODS","TEST_SAMPLE"]
	colection_DEC_code_in_File = [40,41,6,7,173]
	fileText = open('../../listing_address/'+name_file[number_file]+'.list', 'r')
	all_lines = fileText.readlines()
	fileText.close()
	if len(all_lines) == 0:
		FAM = list(bin(int(colection_DEC_code_in_File[number_file])))
		SN = list(bin(int(0)))
		PARTY = list(type_of_party)
	else:
		last_line = all_lines[-1].split(" ")
		FAM = list(bin(int(colection_DEC_code_in_File[number_file])))
		SN = list(bin(int(last_line[2])+1))
		PARTY = list(type_of_party)
	print(len(PARTY))
	pacet_address_str = ""
	pacet_address = 0;
	number_bit = -1
	x = -1
	number_bit = 7 + 2 #0 and 1 bit ("0b") 7+2
	one = ""
	for i in range(2, len(FAM)):
		code[number_bit - i] = int(FAM[int(len(FAM))+1-i])
		one = one + str(code[number_bit - i])
	number_bit = 11
	for i in range(4):
		code[number_bit - i] = int(PARTY[3-i])
		one = one + str(code[number_bit - i])
	number_bit = 55 + 2
	one = one + " "
	for i in range(2, len(SN)):
		code[number_bit - i] = int(SN[int(len(SN))+1-i])
		one = one + str(code[number_bit - i])
	one = one + " "
	step_i = [7,15,23,31,39,47,55]
	flag = True
	for i in step_i:
		number_i = i
		for j in range(8):
			one = one + str(code[number_i-j])
			if crc[0]==code[number_i-j]:
				x = 0
			else:
				x = 1
			crc[0] = crc[1]
			crc[1] = crc[2]
			if crc[3]==x:
				crc[2] = 0
			else: 
				crc[2] = 1
			if crc[4]==x:
				crc[3] = 0
			else:
				crc[3] = 1
			crc[4] = crc[5]
			crc[5] = crc[6]
			crc[6] = crc[7]
			crc[7] = x	
	for i in crc:
		pacet_address_str = pacet_address_str + str(i)
		ishod = ishod + str(i)
	for i in range(56):
		pacet_address_str = pacet_address_str + str(code[55-i])
	iterator = 0
	pacet_list = list(pacet_address_str)
	pacet = ""
	full_pacet_chr = []
	col_pacet_data = 0
	number_element_list = 62
	pacet = pacet + str(pacet_list[63])
	while True:
		iterator = iterator + 1
		if iterator>7:
			pacet_address = chr(int(pacet,2))
			full_pacet_chr.append(pacet_address)
			col_pacet_data = col_pacet_data + 1
			print (pacet)
			if col_pacet_data == 8:
				break
			pacet = ""
			iterator=0
			pacet = pacet + str(pacet_list[number_element_list])
			number_element_list =number_element_list-1
		else:
			pacet = pacet + str(pacet_list[number_element_list])
			number_element_list =number_element_list-1
	ser.write('3')
	ser.write(chr(pin))
	for i in range(len(full_pacet_chr)):
		ser.write(full_pacet_chr[i])
	time.sleep(5)
	return ishod
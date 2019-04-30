import serial
import time
import pylab
import crc8
import numpy
import scipy
import MIT
import test_SMS as sms
import matplotlib.pyplot as plt
import read_the_temperature as rT
import single_chip_setup as scs
import accessory as acc
import calculation as clc
import write_bits as wb
import calculation_OTP as clc_OTP
import one_Use as oU
import test_Yokogawa as Yokogawa
import test_ADDRESS as tADR
from scipy import interpolate

'''
Form array pin_arduino1

'''
def form_array_pin_arduino():
	pin_arduino_array = []
	'''
	22 - start pin_arduino
	53 - finish pin_arduino 
	'''
	for i in range(acc.get_start_arduino_port(), acc.get_finish_arduino_port() + 1):
		pin_arduino_array.append(int(i))
	return pin_arduino_array
	
'''
MAIN FUNCTION
'''
def main_function(ser):
	use_MIT_flag = False
	print ("Use MIT?" + '\n' + "1 - yes" + " 2 - No;")
	commands = int(input())
	if commands == 1:
		use_MIT_flag = True
		print("Write MIT_COM_port ")
		MIT_COM_port = int(input())
		print("Write MIT_start_port ")
		MIT_start_port = int(input())
		print("Write MIT_finish_port")
		MIT_finish_port = int(input())
	elif commands==2:
		MIT_COM_port = 0
		MIT_start_port = 0
		MIT_finish_port = 0
		
	print("Number_family - 1:BMK_GEN (0x28); 2:BMK_DIODS (0x29); 3:CUSTOM_GEN (0x06); 4:CUSTOM_DIODS (0x07); 5:TEST_SAMPLE (0xAD);")
	number_family = str(input())
	print("write type_of_party = ")
	type_of_party = raw_input()
	
	print("start")
	all_temperature = scs.read_all_temperature(ser)
	pin_arduino_array = form_array_pin_arduino()
	# Array work_chip - elements in 1 test
	work_chip_1 = []
	
	#check work chips
	print ("--Start check work chips--")
	for pin_arduino in pin_arduino_array:
		if (scs.circuit_health_check(ser, pin_arduino, all_temperature))==True:
			work_chip_1.append(int(pin_arduino))
		else:
			print("Don't work chip " + str(pin_arduino))
	print ("--Finish check work chips--")
	acc.pause()
	
	print ("--Start write REZ all chip--")
	#write REZ all chip
	scs.set_REZ(ser, work_chip_1)
	print ("--Finish write REZ all chip--")
	#acc.pause()
	
	all_temperature = scs.read_all_temperature(ser)
	# Array work_chip - elements in 2 test
	work_chip_2 = []
	
	#check REZ
	print ("--Start check REZ--")
	for pin_arduino in work_chip_1:
		if (scs.check_REZ(ser, pin_arduino, all_temperature))==True:
			work_chip_2.append(pin_arduino)
		else:
			print("Check REZ failed " + str(pin_arduino))
	print ("--Finish check REZ--")
	acc.pause()
	
	if len(work_chip_2) == 0:
		print ("--No chip--")
		return
		
	#write address
	print ("--Start write address--")
	for pin_arduino in work_chip_2:
		scs.set_address(ser, number_family, type_of_party, pin_arduino)
	
	print ("--Finish write address--")
	acc.pause()
	
	#check address	
	print ("--Finish Check address	--")
	for pin_arduino in work_chip_2:
		if scs.check_address(ser, pin_arduino) == False:
			print("Check ADDRESS failed " + str(pin_arduino))
	print ("--Finish Check address	--")		
	#Read the code and write it to a file.
	print("--Read the code and write it to a file.--")
	main_function_size(ser, MIT_COM_port, MIT_start_port, MIT_finish_port, use_MIT_flag)
	
	pass

'''
read temperature and write in the file
'''
def main_function_size(ser, MIT_COM_port, MIT_start_port, MIT_finish_port, use_MIT_flag):
	for i in range(acc.get_the_number_of_points()):
		#acc.pause_time_read_temperature()
		rT.write_in_file_the_temperature_all_schemes_test(ser, MIT_COM_port, MIT_start_port, MIT_finish_port, use_MIT_flag)
		acc.writeFileAllInOneFile()
		sms.start()
		print("Continue?" + "\n" + "1 -Yes;" + "\n" + "2 - No;")
		commands = input()
		if commands == 2:
			break
	pass
	
'''
Separate setting REZ all chips.
'''
def work_with_REZ(ser):
	pin_arduino_array = form_array_pin_arduino()
	all_temperature = scs.read_all_temperature(ser)
	print ("--Check work chips--")
	work_chip_1 = []
	for pin_arduino in pin_arduino_array:
		if (scs.circuit_health_check(ser, pin_arduino, all_temperature))==True:
			work_chip_1.append(int(pin_arduino))
		else:
			print("Don't work chip " + str(pin_arduino))
	print ("--Check work chips is FINISH--")
	
	if len(work_chip_1)==0:
		print("not work chip")
		return
	
	print ("--Write REZ all chip--")
	#write REZ all chip
	scs.set_REZ(ser, work_chip_1)
	
	#acc.pause()
	
	all_temperature1 = scs.read_all_temperature(ser)
	# Array work_chip - elements in 2 test
	work_chip_2 = []
	
	#check REZ
	print ("--check REZ--")
	for pin_arduino in work_chip_1:
		if (scs.check_REZ(ser, pin_arduino, all_temperature1))==True:
			work_chip_2.append(pin_arduino)
		else:
			print("Check REZ failed " + str(pin_arduino))
	pass
	
'''
Separate setting of addresses of all chips. !!!Do not use very carefully!!!
'''
def work_with_ADDRESS(ser):
	print("Number_family - 1:BMK_GEN (0x28); 2:BMK_DIODS (0x29); 3:CUSTOM_GEN (0x06); 4:CUSTOM_DIODS (0x07); 5:TEST_SAMPLE (0xAD);")
	number_family = str(input())
	print("write type_of_party = ")
	type_of_party = raw_input()
	print(type_of_party)
	pin_arduino_array = form_array_pin_arduino()
	print ("--Write address--")
	for pin_arduino in pin_arduino_array:
		scs.set_address(ser, number_family, type_of_party, pin_arduino)
	acc.pause()
	#check address	
	print ("--Check address	--")
	for pin_arduino in pin_arduino_array:
		scs.check_address(ser, pin_arduino)
	pass

'''
Write OTP
'''
def work_OTP(ser):
	start_address = 2040
	start_KOD = 2992
	for i in range(256):
		print("++")
	pass
	
'''
Program body
'''
print ("Enter the number?" + "\n" + "1 - Yes;" +"\n" + "2 - No (use COM7)")	
commands_control = input()
if commands_control == 1:
	print ("Enter the number port")	
	number_COM_port = input()
else:
	number_COM_port = 7
ser = serial.Serial('COM' + str(number_COM_port), 9600, timeout=0)
ser.close()
ser.open()
ser.isOpen()
flag=True
col_list = []

while True:
	print ("\n" + "-------------------------")
	print ("menu commands:" + "\n" + "1 - main function;" + "\n" + "2 - Temperature reading;" + "\n" + "3 - work with REZ;"  + "\n" + 
	"4 - work with ADDRESS; !!!Do not use very carefully!!!" + "\n" + "5 - Coefficient calculation;" + "\n" + "6 - Check REZ;" + "\n" + 
	"7 - Check ADDRESS;" + "\n" + "8 - Write OTP;" + "\n" + "9 - Form file;" + "\n" + "10 - Read KOD in all chip;" + "\n"  + "11 - init source (8.5V and 5V) and used fire;" + "\n"  + 
	"12 - Write Enable 2;" + "\n"  + "13 - Read address (2 memory ) in one chip;" + "\n"  + "14 - Read address in all chip and write file;" + "\n" + 
	 "0 - EXIT;")
	print ("-------------------------" + "\n")
	print ("enter the commands ")
	commands = str(input())
	if commands=="1":
		main_function(ser)
		break
	elif commands == "2":
		use_MIT_flag = False
		print ("Use MIT?" + '\n' + "1 - yes" + " 2 - No;")
		commands = int(input())
		if commands == 1:
			use_MIT_flag = True
			print("Write MIT_COM_port ")
			MIT_COM_port = int(input())
			print("Write MIT_start_port ")
			MIT_start_port = int(input())
			print("Write MIT_finish_port")
			MIT_finish_port = int(input())
			main_function_size(ser, MIT_COM_port, MIT_start_port, MIT_finish_port, use_MIT_flag)
		elif commands==2:
			main_function_size(ser, 0, 0, 0, use_MIT_flag)
	elif commands == "3":
		work_with_REZ(ser)
	elif commands == "4":
		work_with_ADDRESS(ser)
	elif commands == "5":
		for i in range(acc.get_start_arduino_port(), acc.get_finish_arduino_port() + 1):
			clc.calculation_coefficients(ser, str(i))
	elif commands == "6":
		all_temperature = scs.read_all_temperature(ser)		
		#array_pin_arduino = form_array_pin_arduino()
		#work_chip_2 = []
		#for pin_arduino in array_pin_arduino:
		pin_arduino = 22
		if (scs.check_REZ(ser, pin_arduino, all_temperature))!=True:
			print("Check REZ failed " + str(pin_arduino))
	elif commands == "7":
		#array_pin_arduino = form_array_pin_arduino()
		#for pin_arduino in array_pin_arduino:
		pin_arduino = 22
		if scs.check_address(ser, pin_arduino) == False:
			print("Check ADDRESS failed " + str(pin_arduino))
	elif commands == "8":
		#for i in range(acc.get_start_arduino_port(), acc.get_finish_arduino_port()+1):
		clc_OTP.calculation_ADDRESS_and_KOD(ser)
	elif commands == "9":
		acc.writeFileAllInOneFile()
	elif commands == "10":
		print(scs.read_all_temperature(ser))
	elif commands == "11":
		Yokogawa.init_9V()
		Yokogawa.init_5V()
		time.sleep(1)
		Yokogawa.fire()
	elif commands == "12":
		for i in range(acc.get_start_arduino_port(), acc.get_finish_arduino_port()+1):
			ser.write('5')	
			number_p = chr(int(i) - 22)
			ser.write(number_p)
			#time.sleep(0.5)
			#Yokogawa.fire_9V()
	elif commands == "13":
		for i in range(acc.get_start_arduino_port(), acc.get_finish_arduino_port()+1):
			tADR.give_me_OTP_address(ser, i)
	elif commands == "14":
		tADR.main_read_address_and_form_file_in_all_adderss_on_chip(ser)
		#for i in range(acc.get_start_arduino_port(), acc.get_finish_arduino_port()+1):
		#	address_one_chip_list = tADR.check_address(ser, i)
		#	if (len(address_one_chip_list)>0):
		#		tADR.read_address_on_all_chip_and_write_file(i, address_one_chip_list)
		#	else:
		#		print("port arduino " + str(i) + " ERROR")
	elif commands == "15":
		for i in range(acc.get_start_arduino_port(), acc.get_finish_arduino_port()+1):
			print(acc.check_address_in_chip(ser, i))
	elif commands == "16":
		#for i in range(acc.get_start_arduino_port(), acc.get_finish_arduino_port()+1):
		ser.write('8')
		time.sleep(5)
		print(ser.readlines())
		#tADR.give_number_port(ser)
	elif commands == "0":
		break
	
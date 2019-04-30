import serial
import time
import accessory as acc

'''
'''
def give_me_OTP_address(ser, port):
	fileText = open('../../data/ADDRESS_test_one_chip.txt', 'w')
	fileText.close()
	for i in range(256):
		print(i)
		bit_address = [0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1]
		bit_KOD = str(bin(i))
		bit_KOD = list(bit_KOD[2:len(bit_KOD)])
		iterator = len(bit_KOD) + 2
		for k in bit_KOD:
			bit_address[iterator] = k
			iterator-=1
		byte = ""
		iterator = 0
		package = []
		for bit in bit_address:
			if iterator == 7:
				byte += str(bit)
				package.append(chr(int(byte[::-1],2)))
				byte = ""
				iterator = 0
			else:
				byte += str(bit)
				iterator += 1
		ser.write('8')	
		number_p = chr(int(port) - 22)
		ser.write(number_p)	
		for j in package:
			ser.write(j)
		time.sleep(0.5)
		while True:
			all_lines = ser.readlines()
			if len(all_lines) == 2:
				break
		form_KOD(all_lines, int(i))
	pass

'''

'''	
def form_KOD(list, address):
	low = list[0]
	high = list[1]
	itog_array = []
	for i in range(len(high)-2):
		itog_array.append(high[i])
	for i in range(len(low)-2):
		itog_array.append(low[i])
	#print(high)
	#print(low)
	#kod = ''.join(itog_array)
	kod = ""
	for i in range(4,len(itog_array)):
		kod += str(itog_array[i])
	print(int(kod,2))
	write_File_All_ADDRESS_In_One_Chip(address , int(kod,2))
	print("")
	pass

'''
'''	
def write_File_All_ADDRESS_In_One_Chip(address, kod):
	fileText = open('../../data/ADDRESS_test_one_chip.txt', 'a')
	for i in range(acc.get_start_arduino_port(), acc.get_finish_arduino_port()+1):
		fileText.write(str(address) + " | " + str(kod) + '\n')
	fileText.close()
	pass

'''
'''	
def read_address_on_all_chip_and_write_file(i, list):
	fileText = open('../../data/' + str(i) + '.txt', 'a')
	fileText.write('_'.join(list) + '\n')
	fileText.close()
	pass

'''
'''	
def check_address_12(ser, number_pin_arduino):
	ser.write('4')
	pin = chr(int(number_pin_arduino) - 22)
	ser.write(pin)
	time.sleep(2)
	line = ser.readlines()
	full_address = []
	if len(line) == 9:
		for i in range(1,9):
			address = str(line[i])
			full_address.append(address[0:len(address)-2])
	return full_address
	
# Main read address and form file in all adderss on chip
def main_read_address_and_form_file_in_all_adderss_on_chip(ser):
	fileText = open('../../data/All_address.txt', 'w')
	fileText.close()
	time.sleep(2)
	for port in range(acc.get_start_arduino_port(), acc.get_finish_arduino_port()+1):
		address_str = ""
		address_str = check_address(ser, port)
		read_address_on_all_chip_and_write_file(port, address_str)
	pass
	
# This block need write main_read_address_and_form_file_in_all_adderss_on_chip.
def read_address_on_all_chip_and_write_file(port, address):
	fileText = open('../../data/All_address.txt', 'a')
	address_pin = str(port) + "|" + address
	fileText.write(address_pin + '\n')
	print(address_pin)
	fileText.close()
	pass

# Check address in chip and return "173_16_0_0_0_0_9_135".
def check_address(ser, number_pin_arduino):
	ser.write('4')
	pin = chr(int(number_pin_arduino) - 22)
	ser.write(pin)
	time.sleep(2)
	line = ser.readlines()
	#print(line)
	full_address = []
	if len(line) == 9:
		for i in range(1,9):
			address = str(line[i])
			full_address.append(address[0:len(address)-2])
	address_str_list = '_'.join(full_address)
	return address_str_list

#
def give_number_port(ser):
	port = 22
	file = -1
	address = check_address(ser, port)
	fileText = open('../../data/All_address.txt', 'r')
	for line in fileText:
		port_and_address = line.split("|")
		address_in_file = port_and_address[1]
		print(address_in_file[:len(address_in_file)-1] + " __ " + address)
		if address_in_file[:len(address_in_file)-1] == address:
			file = int(port_and_address[0])
			break
	fileText.close()
	print(file)
	return file
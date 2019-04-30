import visa
import time

'''
Initialization YOKOGAWA 8.5 volt
'''
def init_9V():
	rm = visa.ResourceManager()
	lst = rm.list_resources('?*')
	#print(lst)
	my_instrument = rm.open_resource(lst[0])
	my_instrument.write(":SOUR:FUNC VOLT")
	my_instrument.write(":SOUR:RANGE 10E+0")
	my_instrument.write(":SOUR:LEV 8.3E+0")
	pass

'''
Initialization YOKOGAWA 5.0 volt
'''	
def init_5V():
	rm = visa.ResourceManager()
	lst = rm.list_resources('?*')
	#print(lst)
	my_instrument = rm.open_resource(lst[1])
	my_instrument.write(":SOUR:FUNC VOLT")
	my_instrument.write(":SOUR:RANGE 10E+0")
	my_instrument.write(":SOUR:LEV 5.0E+0")
	pass

'''
Used 8.5 volt
'''
def fire_9V():
	rm = visa.ResourceManager()
	lst = rm.list_resources('?*')
	#print(lst)
	my_instrument = rm.open_resource(lst[0])
	#print(my_instrument)
	my_instrument.write(":OUTP:STAT 1")
	time.sleep(0.5)
	my_instrument.write(":OUTP:STAT 0")
	pass

'''
Used 5.0 volt
'''	
def fire():
	rm = visa.ResourceManager()
	lst = rm.list_resources('?*')
	#print(lst)
	my_instrument = rm.open_resource(lst[1])
	#print(my_instrument)
	my_instrument.write(":OUTP:STAT 1")
	time.sleep(0.5)
	fire_9V()
	time.sleep(0.5)
	my_instrument.write(":OUTP:STAT 0")
	pass

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
import test_Yokogawa as Yokogawa
import test_ADDRESS as tADR
from scipy import interpolate

print(clc.readFile("22"))
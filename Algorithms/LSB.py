import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile as wav
from scipy.fftpack import fft, fftfreq, ifft, rfft, rfftfreq, irfft
import binascii
import cmath as cm
import math as m

def parse_audio(filename):
    rate, data = wav.read(filename)
    data = data.T[0]
    if data.dtype =='int8':
        data = data / (2.**7)
    time_array = np.arange(0, data.shape[0],1)/rate
    length = time_array[-1]
    # plt.plot(time_array, data)
    # plt.xlabel('Time (s)')
    # plt.ylabel('Amplitude')
    # plt.title(str(filename))
    # plt.show()
    return time_array, data, rate
def convertmessage(message): #Converts message to a binary form.
    bin_msg = []
    bin_msg.append(''.join(format(ord(x), 'b') for x in message))
    print(bin_msg)
    return bin_msg
def lsb_of_audio(data, bin_msg):
    bin_data = []
    tick = len(bin_msg)
    for value in range(len(data)):
        # bin_data.append(bin( int(data[value]) + int(bin_msg[value])))
        bin_data.append(bin( int(data[value])))
        tick -= 1
        if tick == 0:
            for x in range(value +1,len(data)):
                bin_data.append(bin(int(data[x])))
            break
    return bin_data
         
def encoded_file(time, data):
    newdata = []
    for i in range(len(data)):
        newdata.append((int(data[i], 8)))
    plt.plot(time, newdata)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Encoded AUdio FIle')
    plt.show()

def encode(filename, message):
    time_array, data, rate = parse_audio(filename)
    bin_msg = convertmessage(message)
    bin_data = lsb_of_audio(data, bin_msg)
    encoded_file(time_array,bin_data)

encode("bell1.wav", "Hello")
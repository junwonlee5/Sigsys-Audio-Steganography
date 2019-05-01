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
    # if data.dtype =='int8':
    #     data = data / (2.**7)

    print(data.shape[0])
    time_array = np.arange(0, data.shape[0],1)/rate
    length = time_array[-1]

    return time_array, data, rate

def convertmessage(message): #Converts message to a binary form.
    bin_msg = []
    # for letter in message:
        # bin_msg.append((format(ord(letter), 'b')))
    bin_msg.append(''.join(format(ord(x), 'b') for x in message))
    for i in range(len(bin_msg[0])):
        bin_msg.append(bin_msg[0][i])
            
    bin_msg = bin_msg[1:]
    return bin_msg

    
def lsb_of_audio(data, bin_msg):
    bin_data =[]
    tick = len(bin_msg)
    for i in range(len(data)):
        new = bin(data[i])
        newnew = new.replace('b','')
        bin_data.append(bin(int(newnew,2) + int(bin_msg[i],2)))
        tick -= 1
        if tick == 0:
            for x in range(i +1,len(data)):
                bin_data.append(bin(int(data[x])))
            break
    return bin_data
         
def encoded_file(time, data):
    newdata = []
    for i in range(len(data)):
        data[i] = data[i].replace('b','')
        newdata.append(int(data[i],2))
    plt.plot(time, newdata)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Encoded AUdio FIle')
    plt.savefig('EncodedAudiofile-LSB.png')
    return newdata

def decode(encodeddata):
    encoded, time = encodeddata
    binencoded = []
    lsb = []
    for i in range(len(encoded)):
        binencoded.append(bin(encoded[i]))
        lsb.append(binencoded[i][-1])
        
    lsb = ''.join(lsb)
    lsb = [lsb[i:i+8] for i in range(0,len(lsb), 8)]
    message = 
def encode(filename, message):
    time_array, data, rate = parse_audio(filename)
    bin_msg = convertmessage(message)
    bin_data = lsb_of_audio(data, bin_msg)
    encoded = encoded_file(time_array,bin_data)

    return encoded,time_array


    # decode(encoded)
decode(encode("bell1.wav", "Hello"))

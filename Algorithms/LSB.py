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
    time_array = np.arange(0, data.shape[0],1)/rate
    return time_array, data, rate

def convertmessage(message): #Converts message to a binary form.
    bin_msg = []
    fmsg = []
    for x in message:
        bin_msg.append(bin(ord(x))[2:].zfill(8))
    bin_msg = "".join(bin_msg)

    for ch in bin_msg:
        fmsg.append(ch)
    
    return fmsg
    
def binary_audio(data):  ## Returns the audio in binary
    binarydata = []
    for i in range(len(data)):
        binary = bin(data[i])
        binarydata.append(str(binary))
        
    return binarydata

def encode_data(binarydata, message):  ##encodes message into file using LSB
    encoded = []
    for i in range(len(message)-1):
        if binarydata[i][-1] == message[i]:
            encoded.append(binarydata[i])
        elif binarydata != message[i]:
            b = list(binarydata[i])
            b[-1] = message[i]
            b = "".join(b)
            encoded.append(b)
    for i in range(len(message)-1,len(binarydata)):
        nob = binarydata[i]
        nob = nob.replace('0b','')
        encoded.append(nob)
    return encoded


def plot_encoded_file(filename, rate, time, data):  ## Plots and saves encoded audio file
    newdata = []
    for i in range(len(data)):
        data[i] = data[i].replace('b','')
        newdata.append(int(data[i],2))
    plt.plot(time, newdata)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Encoded AUdio FIle')
    plt.savefig('EncodedAudiofile-LSB.png')
    wav.write('LSB_modified'+str(filename), rate, data)


def decode(encodeddata):
    message = []
    lsb = []
    for i in range(40):
        lsb.append(encodeddata[i][-1])
    
    lsb = ''.join(lsb)

    n = 8
    lsb = [lsb[i:i+n] for i in range(0,len(lsb),n)]
    print(lsb)
    for i in range(len(lsb)):
        message.append(chr(int(lsb[i], 2)))
    print(message[0:100])


def encode(filename, message):
    time_array, data, rate = parse_audio(filename)
    bin_msg = convertmessage(message)
    binarydata = binary_audio(data)
    encoded = encode_data(binarydata,bin_msg)
    plot_encoded_file(filename, rate, time_array,encoded)
    decode(encoded)

    # decode(encoded)
encode("bell1.wav", "abcde")

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

    encodedfile = open("encodedLSB.txt","w")
    encodedfile.write(str(encoded).replace('0b',''))
    return encoded

def plot_encoded_file(filename,time, rate, data):  ## Plots and saves encoded audio file
    newdata = []
    for i in range(len(data)):
        data[i] = data[i].replace('b','')
        newdata.append(int(data[i],2))
    plt.plot(time, newdata)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Encoded Audio File')
    plt.savefig('EncodedAudiofile-LSB.png')
    # wavefile.write('LSB modified'+str(filename) , rate, data)
    arr = np.int16(newdata)
    wav.write('LSB_modified'+str(filename), 44100, arr)

def decode(filename):
    binary = []
    message = []
    lsb = []
    dataq = []
    rate, data = wav.read(filename)
    data.tolist()
    for i in range(len(data)):
        binary.append(bin(data[i]))
    for i in range(len(binary)):
        lsb.append(binary[i][-1])
    lsb = ''.join(lsb)
    lsb = [lsb[i:i+8] for i in range(0,len(lsb),8)]
    for i in range(len(lsb)):
        message.append(chr(int(lsb[i], 2)))
    message = list(message)
    message = ''.join(message)
    decodedfile = open("decodedfile.txt","w")
    decodedfile.write(str(message))
    


def encode(filename, message):
    time_array, data, rate = parse_audio(filename)
    bin_msg = convertmessage(message)
    binarydata = binary_audio(data)
    encoded = encode_data(binarydata,bin_msg)
    plot_encoded_file(filename, time_array,rate,encoded)
    return encoded
encode("bell1.wav", "According to all known laws of aviation, there is no way that a bee should be able to fly. Its wings are too small to get its fat little body off the ground. The bee, of course, flies anyways. Because bees don't care what humans think is impossible.")
decode('LSB_modifiedbell1.wav')
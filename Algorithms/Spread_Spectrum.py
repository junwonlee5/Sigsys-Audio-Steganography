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
    if data.dtype =='int16':
        data = data / (2.**15)
    #print(data.shape[0])
    time_array = np.arange(0, data.shape[0],1)/rate
    length = time_array[-1]
    #print(len(time_array), len(data), time_array[-1])
    #plt.plot(time_array, data)
    #plt.xlabel('Time (s)')
    #plt.ylabel('Amplitude')
    #plt.title(str(filename))
    #plt.show()
    return time_array, data, rate

def run_fft(filename):
    time_array, data, rate= parse_audio(filename)
    T = 1/rate;
    N = len(time_array)
    X = rfft(data)
    freqs = rfftfreq(len(data)) * rate
    phase = np.angle(X)
    orig_data = irfft(X)
    #plt.figure(1)
    #plt.subplot(311)
    #plt.plot(freqs, 2*abs(X)/N)
    #plt.subplot(312)
    #plt.plot(freqs, phase)
    #plt.subplot(313)
    #plt.plot(time_array, orig_data)
    #plt.show()
    return X, freqs, phase, time_array, rate, data

    #wav.write('modifiedbell1.wav', rate, orig_data)

def rewrite(filename, code):
    X, freqs, phase, time_array, rate, data = run_fft(filename)
    code_bin = bin(int.from_bytes(code.encode(), 'big'))
    #print(code_bin)
    code_bin = code_bin[2:]
    binary_list = [int(d) for d in str(code_bin)]
    #print(binary_list)
    for a in range(len(binary_list)):
        if binary_list[a] == 1:
            X[a] = X[a]*1.01
        elif binary_list[a] == 0 :
            X[a] = X[a]*0.99
    for b in range(len(X)):
        X[b] = abs(X[b])*np.exp(np.angle(X[b])*1j)
    orig_data = irfft(X)
    #plt.plot(time_array, orig_data)
    #plt.show()
    wav.write('modified2'+str(filename) , rate, orig_data)
    return orig_data, X, rate,time_array, binary_list
def decode(filename, code):
    orig_data, X2, rate, time_array, binary_list = rewrite(filename, code)
    X, freqs, phase2, time_array, rate, data = run_fft(filename)
    freq_diff = X/X2
    #print(freq_diff[0:len(binary_list)])
    bin_code = []
    for a in range(len(freq_diff[0:len(binary_list)])):
        if round(freq_diff[a], 2) == 0.99:
            #print(a, freq_diff[a], '1')
            bin_code.append('1')
        elif round(freq_diff[a], 2)  == 1.01:
            #print(a, freq_diff[a], '0')
            bin_code.append('0')
        else:
            print(a, freq_diff[a])
    bin_string = '0b' + ''.join(bin_code)
    #print(bin_string)
    n = int(bin_string, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()
print(decode('bell1.wav', 'Junwon Lee'))

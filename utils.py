import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

def logistic_map(x,A):
    return A*x*(1-x)
def logistic_map_derivative(x,A):
    return A[:,np.newaxis]*(1-2*x)

def quadratic_map(x,A):
    return 1-A*x*x
def quadratic_map_derivative(x,A):
    return -2*A[:,np.newaxis]*x

def biquadratic_map(x,A):
    return 1-A*x**4
def biquadratic_map_derivative(x,A):
    return -4*A[:,np.newaxis]*x**3

def sine_map(x,A):
    return A*np.sin(x)
def sine_map_derivative(x,A):
    return A[:,np.newaxis]*np.cos(x)

def evolution(x0, A, t, arr_size=None,chosen_map=logistic_map):
    if not arr_size:
        arr_size = t
    x = np.zeros(shape=(len(A),arr_size))
    x[:,0] = x0
    prev = x[:,0]
    for i in range(1,t):
        # if i%100==0:
            # print(f"simulated {i} steps")
        x[:,i%arr_size] = chosen_map(prev,A)
        prev = x[:,i%arr_size]
    if arr_size:
        x = np.hstack((x[:,t%arr_size:],x[:,:t%arr_size]))
    return x

def calculate_periods(asymptotic_trajectory,A):
    f, Pxx_den = signal.periodogram(asymptotic_trajectory,fs=1,axis=1,return_onesided=False)
    periods = []
    for i in range(len(A)):
        peaks,_ = signal.find_peaks(np.log10(Pxx_den[i,:]),height=-10)
        peaks = f[peaks]
        if len(peaks) == 0:
            T = 1
        else:
            T = round(1/min(abs(peaks)))
        periods.append(T)
    return np.array(periods)
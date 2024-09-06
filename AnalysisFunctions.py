import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# fit amplitude
def A(f,k,m,c,F0):
    omega_0 = np.sqrt(k/m)
    ksi = c/(2*np.sqrt(m*k))
    omega = 2*np.pi*f
    return F0/(m*np.sqrt((2*omega*omega_0*ksi)**2+(omega_0**2-omega**2)**2))


def A(f,ksi,omega_0,A0):
    omega = 2*np.pi*f
    return A0/(np.sqrt((2*omega*omega_0*ksi)**(2)+(omega_0**(2)-omega**(2))**(2)))

def gauss(x, H, A, x0, sigma):
    return H + A * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2))


# fit phase
def phase(f,f0,ksi,offset=0):
    print(f0)
    return np.arctan((2*f*f0*ksi)/(f**2 - f0**2)) + offset

# calcualte displacment in nm from amplitude in volts
import numpy as np

# Calculate displacement in nm from amplitude in volts
def calcX(V, f):
    X = []
    for v, freq in zip(V, f):
        X.append(((v * np.sqrt(2)) * 9.80665 * 10 ** 9) / (0.22 * (2 * np.pi * freq) ** 2))
    return X

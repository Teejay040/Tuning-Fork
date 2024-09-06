# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 15:01:33 2022

@author: jjagiel

This program is for using the tuning fork and controlling the piezo and the Arduino at the same time.
"""

import numpy as np
import matplotlib.pyplot as plt
import time
import os
from tkinter import simpledialog
import csv

datecreate = simpledialog.askstring('Input', 'Enter the date name')
fichier = simpledialog.askstring('Input', 'Enter the files name')

import pi_e_625
p = pi_e_625.pi_e_625()

import sfa
s = sfa.sfa()

time.sleep(5)
s.Sa(0.1)
s.sSa(0.004)
time_measurement = 100  # Measurement duration in seconds
fixed_frequency = 850  # Fixed frequency in Hz

def DataDump(filename, duration, num_points=100):
    """
    This function saves the data: frequency, amplitude driving, 
    amplitude output, phase, for shear and normal during a defined 
    time measurement.
    """
    file = open(filename, "w")
    
    timestamps = []
    amplitudes_mesure_n = []
    amplitudes_consigne_n = []
    phases_normal = []
    amplitudes_mesure_s = []
    amplitudes_consigne_s = []
    phases_shear = []
    rapport_amplitudes_n = []
    rapport_amplitudes_s = []
    
    interval = duration / num_points  # Interval time between points
    
    for i in range(num_points):
        fd_n = float(s.Rf())
        fd_s = float(s.sRf())
        ad_n = float(s.Ra())
        ad_s = float(s.sRa())
        
        am_n = float(s.Rm())
        am_s = float(s.sRm())
        
        pd_n = float(s.Rp())
        pd_s = float(s.sRp())
        
        # Calculate amplitude ratios
        rapport_n = am_n / am_s if am_s != 0 else 0
        rapport_s = am_s / am_n if am_n != 0 else 0
        
        file.write(f"{fd_n},{ad_n},{am_n},{pd_n},{fd_s},{ad_s},{am_s},{pd_s},{rapport_n},{rapport_s}\n")
        
        timestamps.append(i * interval)
        amplitudes_mesure_n.append(am_n)
        amplitudes_consigne_n.append(ad_n)
        phases_normal.append(pd_n)
        amplitudes_mesure_s.append(am_s)
        amplitudes_consigne_s.append(ad_s)
        phases_shear.append(pd_s)
        rapport_amplitudes_n.append(rapport_n)
        rapport_amplitudes_s.append(rapport_s)
        
        time.sleep(interval)  # Wait for the next interval
    
    file.close()
    return timestamps, amplitudes_mesure_n, amplitudes_consigne_n, phases_normal, amplitudes_mesure_s, amplitudes_consigne_s, phases_shear, rapport_amplitudes_n, rapport_amplitudes_s

def SaveToCSV(csv_filename, timestamps, amplitudes_mesure_n, amplitudes_consigne_n, phases_normal, amplitudes_mesure_s, amplitudes_consigne_s, phases_shear, rapport_amplitudes_n, rapport_amplitudes_s):
    """
    This function saves the collected data into a CSV file.
    """
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'Amplitude Mesuree Normal', 'Amplitude Consignee Normal', 'Phase Normal', 
                         'Amplitude Mesuree Shear', 'Amplitude Consignee Shear', 'Phase Shear', 
                         'Rapport Amplitude Normal', 'Rapport Amplitude Shear'])
        
        for i in range(len(timestamps)):
            writer.writerow([timestamps[i], amplitudes_mesure_n[i], amplitudes_consigne_n[i], phases_normal[i], 
                             amplitudes_mesure_s[i], amplitudes_consigne_s[i], phases_shear[i], 
                             rapport_amplitudes_n[i], rapport_amplitudes_s[i]])

###########################    
## Begin of the program ##
###########################
Date = datecreate
First_folder = fichier

os.makedirs(Date + '\\' + First_folder)

# Setting the fixed frequency
s.Sf(fixed_frequency)

# Measuring and saving data
filename = Date + '\\' + First_folder + '\\' + 'amplitude_data.txt'
timestamps, amplitudes_mesure_n, amplitudes_consigne_n, phases_normal, amplitudes_mesure_s, amplitudes_consigne_s, phases_shear, rapport_amplitudes_n, rapport_amplitudes_s = DataDump(filename, time_measurement, num_points=100)

# Saving data to CSV
csv_filename = Date + '\\' + First_folder + '\\' + 'amplitude_data.csv'
SaveToCSV(csv_filename, timestamps, amplitudes_mesure_n, amplitudes_consigne_n, phases_normal, amplitudes_mesure_s, amplitudes_consigne_s, phases_shear, rapport_amplitudes_n, rapport_amplitudes_s)

# Plotting the amplitude and phase data
fig, axs = plt.subplots(3, 1, figsize=(12, 18))  # 3 subplots

# Amplitude over time plot (normal and shear)
axs[0].plot(timestamps, amplitudes_mesure_n, label='Amplitude Mesurée Normal', color='blue')
axs[0].plot(timestamps, amplitudes_consigne_n, label='Amplitude Consigne Normal', color='red')
axs[0].plot(timestamps, amplitudes_mesure_s, label='Amplitude Mesurée Shear', color='green')
axs[0].plot(timestamps, amplitudes_consigne_s, label='Amplitude Consigne Shear', color='orange')
axs[0].set_xlabel('Time (s)')
axs[0].set_ylabel('Amplitude')
axs[0].set_title('Amplitude vs Time')
axs[0].legend()
axs[0].grid(True)

# Phase over time plot (normal and shear)
axs[1].plot(timestamps, phases_normal, label='Phase Normal', color='blue')
axs[1].plot(timestamps, phases_shear, label='Phase Shear', color='purple')
axs[1].set_xlabel('Time (s)')
axs[1].set_ylabel('Phase')
axs[1].set_title('Phase vs Time')
axs[1].legend()
axs[1].grid(True)

# Amplitude ratio over time plot (normal and shear)
axs[2].plot(timestamps, rapport_amplitudes_n, label='Rapport Amplitude Normal', color='blue')
axs[2].plot(timestamps, rapport_amplitudes_s, label='Rapport Amplitude Shear', color='green')
axs[2].set_xlabel('Time (s)')
axs[2].set_ylabel('Rapport Amplitude')
axs[2].set_title('Rapport Amplitude vs Time')
axs[2].legend()
axs[2].grid(True)

# Show the plots
plt.tight_layout()
plt.show()

print("Rapport Amplitudes Normal:")
print(rapport_amplitudes_n)
print("Rapport Amplitudes Shear:")
print(rapport_amplitudes_s)

s.serial.close()

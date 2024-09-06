# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 13:36:07 2021

@author: Julie
"""

from scipy import *
from pylab import *
from numpy import *
import numpy as np
import re
from scipy.optimize import curve_fit
import os
from tkinter import filedialog
from tkinter import Tk

from AnalysisFunctions import *

# Function to select a directory
def select_directory():
    root = Tk()
    root.withdraw()  # Hide the root window
    directory = filedialog.askdirectory(title="Select Folder")
    return directory

print('Which frequency do you have changed ? Normal or Shear')
frequency_change = input()

#######################################
## Select the directory for files   ##
#######################################

dirname = select_directory()
if not dirname:
    print("No directory selected. Exiting.")
    exit()

Fichlist = np.array([dirname + os.sep + t for t in os.listdir(dirname) if os.path.isfile(os.path.join(dirname, t)) and t.split('.')[-1] == 'txt'])

# Parameters to save
fn_save, An_save, phin_save, An2_save, fs_save, As_save, phis_save, As2_save = [], [], [], [], [], [], [], []

#######################################################
###              Define the parameter D             ###
### (need to change for each experiment) D is on µm ###
#######################################################

# Example of D values (adjust as needed)
D = [0, -10, -20, -30, -40, -50, -60, -70, -80, -90]

###################################################################
###                Begin of the loop for txt files              ###
###################################################################

for fname in Fichlist:
    #######################################
    ##         Define parameters         ##
    #######################################

    fn, An, phin, An2, fs, As, phis, As2 = [], [], [], [], [], [], [], []
    
    with open(fname, 'r') as f:
        f.readline()  # Skip header line

        for ligne in f:
            mots = ligne.split(',')
            mots = [re.sub('\n', '', mot) for mot in mots]
            fn.append(float(mots[0]))
            An.append(float(mots[1]))
            phin.append(float(mots[3]))
            An2.append(float(mots[2]))

            fs.append(float(mots[4]))
            As.append(float(mots[5]))
            phis.append(float(mots[7]))
            As2.append(float(mots[6]))

    # Append all data points without averaging
    fn_save.extend(fn)
    An_save.extend(An)
    phin_save.extend(phin)
    An2_save.extend(An2)

    fs_save.extend(fs)
    As_save.extend(As)
    phis_save.extend(phis)
    As2_save.extend(As2)

#####################################
###           Some plots          ###
#####################################

def plot_segments(x_data, y_data, xlabel_text, ylabel_text, title):
    num_points = len(x_data)
    num_segments = (num_points + 99) // 100  # Calculate the number of segments of 100 points
    colors = plt.cm.viridis(np.linspace(0, 1, num_segments))  # Generate a color map

    plt.figure(title)
    for i in range(num_segments):
        start = i * 100
        end = start + 100
        plt.plot(x_data[start:end], y_data[start:end], 'o-', color=colors[i % num_segments])

    plt.xlabel(xlabel_text)
    plt.ylabel(ylabel_text)
    plt.title(title)
    plt.show()

if fn_save:
    fn_save = np.array(fn_save)
    An_save = np.array(An_save)
    phin_save = np.array(phin_save)
    An2_save = np.array(An2_save)
    fs_save = np.array(fs_save)
    As_save = np.array(As_save)
    phis_save = np.array(phis_save)
    As2_save = np.array(As2_save)
    
    ### Shear frequency change ###
    if frequency_change == "Shear":
        plot_segments(fs_save, As2_save, "Shear frequency [Hz]", "Shear amplitude [V]", 'Shear Amplitude')
        plot_segments(fs_save, An2_save, "Shear frequency [Hz]", "Normal amplitude [V]", 'Normal Amplitude')
        plot_segments(fs_save, phis_save, "Shear frequency [Hz]", "Shear Phase", 'Phase')
        plot_segments(fs_save, As_save, "Shear frequency [Hz]", "Shear amplitude driving [V]", 'Amplitude')
    
    ### Normal frequency change ###
    if frequency_change == "Normal":
        plot_segments(fn_save, An2_save, "Normal frequency [Hz]", "Normal amplitude [nm]", 'Normal Amplitude')
        plot_segments(fn_save, As2_save, "Normal frequency [Hz]", "Shear amplitude [V]", 'Shear Amplitude')
        plot_segments(fn_save, phin_save, "Normal frequency [Hz]", "Normal Phase", 'Phase')
        plot_segments(fn_save, An_save, "Normal frequency [Hz]", "Normal amplitude driving [V]", 'Amplitude driving')
        
        ###################################
        ##      Curve Fit to find Q      ##
        ###################################
        
        # Additional code for curve fitting can be added here if needed.

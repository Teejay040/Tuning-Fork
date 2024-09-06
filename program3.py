import numpy as np
import matplotlib.pyplot as plt
import time
import os
import tkinter as tk
from tkinter import simpledialog
from scipy import *
from pylab import *
from numpy import *
import re
from scipy.optimize import curve_fit

from AnalysisFunctions import *

import os
from os import path as os_path
from tkinter import filedialog

import pi_e_625
p = pi_e_625.pi_e_625()

import sfa
s = sfa.sfa()



def DataDump(filename, time_measurement):
    """
    This function is for saving the data: frequency, amplitude driving,
    amplitude output, phase. For the shear and the normal during one defined
    time measurement.
    """
    with open(filename, "a") as file:
        for i in range(time_measurement):
            fd_n = float(s.Rf())
            fd_s = float(s.sRf())
            ad_n = float(s.Ra())
            ad_s = float(s.sRa())
            
            am_n = float(s.Rm())
            am_s = float(s.sRm())
            
            pd_n = float(s.Rp())
            pd_s = float(s.sRp())
            
            file.write(f"{fd_n},{ad_n},{am_n},{pd_n},{fd_s},{ad_s},{am_s},{pd_s}\n")
            time.sleep(1)

def run_experiment(voltage):
    datecreate = date_entry.get()
    fichier = file_entry.get()
    fn_min = int(fn_min_entry.get())
    fn_max = int(fn_max_entry.get())
    Number_points = int(num_points_entry.get())
    num = 20
    
    time_measurement = 5
    fn = np.linspace(fn_min, fn_max, num)

    D = []
    
    Date = datecreate
    First_folder = fichier

    output_filename = os.path.join(Date, f"{First_folder}.txt")
    
    # Ensure the output directory exists
    os.makedirs(Date, exist_ok=True)

    with open(output_filename, "w") as file:
        file.write("fd_n,ad_n,am_n,pd_n,fd_s,ad_s,am_s,pd_s\n")  # Write header

    n = 0
    while n <= Number_points:
        D = D + [p.request_voltage()]
        
        try:
            for i in fn:
                time.sleep(5)
                s.Sf(i)
                DataDump(output_filename, time_measurement)
        except Exception:
            s.serial.close()
        
        print(D)
        p.relative_voltage(voltage)  # Use the specified voltage value
        time.sleep(1)
        n += 1
    
    s.serial.close()

# Create the main window
root = tk.Tk()
root.title("THE TUNING FORK")

# Request voltage value at the start
voltage = simpledialog.askfloat("Input", "Enter the desired voltage:", parent=root, minvalue=0.0, maxvalue=120.0)

if voltage is None:
    print("No voltage entered. Exiting...")
    root.destroy()
    exit()

# Create and place labels and entry widgets
tk.Label(root, text="Enter the folder name").grid(row=0, column=0)
date_entry = tk.Entry(root)
date_entry.grid(row=1, column=0)

tk.Label(root, text="Enter the file name").grid(row=2, column=0)
file_entry = tk.Entry(root)
file_entry.grid(row=3, column=0)

tk.Label(root, text="Enter min frequency (Hz)").grid(row=0, column=1)
fn_min_entry = tk.Entry(root)
fn_min_entry.grid(row=1, column=1)

tk.Label(root, text="Enter max frequency (Hz)").grid(row=2, column=1)
fn_max_entry = tk.Entry(root)
fn_max_entry.grid(row=3, column=1)

tk.Label(root, text="Enter number of cycles").grid(row=0, column=2)
num_points_entry = tk.Entry(root)
num_points_entry.grid(row=1, column=2)

# Create and place the start button
start_button = tk.Button(root, text="Start", command=lambda: run_experiment(voltage))
start_button.grid(row=2, column=2, rowspan=2)

# Start the Tkinter event loop
root.mainloop()

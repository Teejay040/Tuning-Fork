# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 15:01:33 2022
"""

import numpy as np
import time
import os
import pi_e_625
import sfa

def run_program(datecreate, fichier):
    # Initialize devices
    p = pi_e_625.pi_e_625()
    s = sfa.sfa()

    # Wait before starting
    time.sleep(5)
    s.Sa(0.1)
    s.sSa(0.004)
    fixed_frequency = 850  # Fixed frequency in Hz

    Date = datecreate
    First_folder = fichier
    os.makedirs(Date + '\\' + First_folder)

    # Setting the fixed frequency
    s.Sf(fixed_frequency)

    # Set initial voltage to 0V before starting measurements
    initial_voltage = 0.0  # Initial voltage for E625
    p.absolute_voltage(initial_voltage)

    # Wait briefly to ensure the voltage is set
    time.sleep(1)

    # Initialize variables
    initial_amplitude = float(s.Rm())  # Store the initial amplitude
    voltage_increment = 1.0  # Voltage increment

    while True:
        current_amplitude = float(s.Rm())
        print(f"Current Amplitude: {current_amplitude}")
        p.absolute_voltage(initial_voltage)
        print(f"Voltage set to: {initial_voltage}V")

        if abs(current_amplitude - initial_amplitude) >= 0.01:
            print("Contact detected!")
            break

        initial_voltage += voltage_increment

        time.sleep(1)  # Wait 1 second before the next measurement

    s.serial.close()

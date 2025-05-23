import numpy as np
import time
import sfa  # Ensure sfa.py is in the same directory

def find_resonance(controller, freq_min=750, freq_max=840,
                   sweep_points=20, tol=1e-3, max_iterations=25, gamma=15):
    """
    Find the resonance frequency using a PLL approach via the sfa controller.
    
    The amplitude sweep uses the measured amplitude (Rm) to pick an initial guess.
    The PLL loop reads the phase (Rp) and converts it to radians. Resonance is
    defined as when the phase error is near zero.
    """
    # 1. Amplitude sweep using measured amplitude (Rm).
    freqs = np.linspace(freq_min, freq_max, sweep_points)
    amplitudes = []
    for f in freqs:
        controller.Sf(f)
        time.sleep(0.5)  # Amplitude measurement delay
        amp_str = controller.Rm().strip()
        print(f"Raw measured amplitude response at {f:.1f} Hz: {repr(amp_str)}")
        try:
            amp = float(amp_str)
        except ValueError:
            print(f"Warning: Could not convert measured amplitude '{amp_str}' to float.")
            amp = 0.0
        amplitudes.append(amp)
    amplitudes = np.array(amplitudes)
    best_index = np.argmax(amplitudes)
    f_res_guess = freqs[best_index]
    current_freq = f_res_guess
    print(f"Initial guess from amplitude sweep: {current_freq:.3f} Hz")
    
    # Proportional gain (gamma = guess atm!)
    Kp = gamma / (4 * np.pi)
    print(f"Using proportional gain: Kp = {Kp:.5f} Hz per radian")
    
    # 2. PLL loop
    for i in range(max_iterations):
        controller.Sf(current_freq)
        time.sleep(0.75)  # Phase measurement delay
        phase_str = controller.Rp().strip()
        try:
            measured_phase_deg = float(phase_str)
        except ValueError:
            print(f"Warning: Could not convert phase '{phase_str}' to float.")
            measured_phase_deg = 0.0
        
        # Convert phase to radians
        error = np.deg2rad(measured_phase_deg)
        print(f"Iteration {i:3d}: Frequency = {current_freq:.6f} Hz, "
              f"Phase = {measured_phase_deg:.2f} deg, "
              f"Phase error = {error:.6f} rad")
        
        # Check error tolerance
        if abs(error) < tol:
            print(f"PLL converged after {i} iterations with frequency {current_freq:.6f} Hz")
            break
        
        # Update the frequency using the error
        current_freq = current_freq + Kp * error
    else:
        print("Maximum iterations reached without full convergence in the PLL loop.")
    
    return current_freq

if __name__ == "__main__":
    # Create an instance of the sfa class.
    controller = sfa.sfa()
    
    # Enable data streaming if required.
    controller.Ed(1)
    time.sleep(3.0)
    
    # Run the PLL routine to estimate the resonance frequency.
    resonance_freq = find_resonance(controller, gamma=15)
    print(f"Final estimated resonance frequency: {resonance_freq:.6f} Hz")
    
    # Close the serial connection.
    controller.serial.close()

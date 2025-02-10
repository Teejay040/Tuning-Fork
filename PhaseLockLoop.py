import numpy as np
import time
import sfa as ssfa

# =============================================================================
# 1. Commander
# =============================================================================


def send_command(command):
    """
    Stub for sending a command string to the controller and reading a reply.
    Replace this stub with your actual communication code (e.g. using pyserial,
    sockets, etc.).
    
    For example, to set the normal frequency you would send: "Sf(850);"
    and to read the current phase you would send: "Rp;".
    """
    # For debugging we simply print the command.
    print("Sending command:", command)
    
    # --- For testing/demo purposes we return a dummy response.
    # (In your real code the response should be read from your hardware.)
    if command.startswith("Ra"):
        # Return a dummy amplitude value.
        return "1.0"
    elif command.startswith("Rp"):
        # Return a dummy phase value.
        return "-1.57"
    elif command.startswith("Rf"):
        # Return a dummy frequency.
        return "850.0"
    else:
        # For commands that only set a parameter, no reply is needed.
        return ""

# =============================================================================
# 2. Controller
# =============================================================================


class ControllerTuningFork:
    def __init__(self, gamma):
        """
        Parameters:
          gamma (float): The damping constant (bes guess or known from calibration) 
          used to compute the optimal PLL gain.
        """
        self.gamma = gamma

    def set_frequency(self, freq):
        """Sets the normal frequency using the controller command 'Sf(x);'."""
        cmd = f"Sf({freq});"
        send_command(cmd)
        time.sleep(0.01)  # 10 ms delay (adjust as needed)

    def get_amplitude(self):
        """Reads the normal amplitude using the command 'Ra;'."""
        cmd = "Ra;"
        response = send_command(cmd)
        try:
            return float(response)
        except ValueError:
            raise ValueError("Invalid amplitude response from controller")

    def get_phase(self):
        """Reads the normal phase (in radians) using the command 'Rp;'."""
        cmd = "Rp;"
        response = send_command(cmd)
        try:
            return float(response)
        except ValueError:
            raise ValueError("Invalid phase response from controller")

    def get_frequency(self):
        """Reads the current normal frequency using the command 'Rf;'."""
        cmd = "Rf;"
        response = send_command(cmd)
        try:
            return float(response)
        except ValueError:
            raise ValueError("Invalid frequency response from controller")

# =============================================================================
# 3. PhaseLockLoop
# =============================================================================


def find_resonance(controller, freq_min=800, freq_max=900,
                   sweep_points=100, tol=1e-3, max_iterations=25):
    """
    Find the resonance frequency using a PLL approach and the real controller.
    
    Steps:
      1. Sweep a frequency range (default 800–900 Hz) in "sweep_points=?" steps (default 100) and choose the frequency
         that gives the highest amplitude (using command Ra;).
      2. Use a PLL loop that adjusts the frequency according to:
      
             f_new = f_old + Kp * (phase error)
      
         where Kp = gamma / (4π).
      3. Stop when the measured phase using Rp;
         is below the tolerance "tol=?" (default 1e-3 rad).
    
    Parameters:
      controller    : instance of ControllerTuningFork.
      freq_min      : lower bound for the initial sweep (Hz)
      freq_max      : upper bound for the initial sweep (Hz)
      sweep_points  : number of points in the sweep.
      tol           : tolerance for the phase error (radians).
      max_iterations: maximum iterations allowed in the PLL loop.
    
    Returns:
      The estimated resonance frequency.
    """
    # --- 1. Initial amplitude sweep.
    freqs = np.linspace(freq_min, freq_max, sweep_points)
    amplitudes = []
    for f in freqs:
        controller.set_frequency(f)
        # (Again, if necessary, add a delay here.)
        amp = controller.get_amplitude()
        amplitudes.append(amp)
    amplitudes = np.array(amplitudes)
    best_index = np.argmax(amplitudes)
    f_res_guess = freqs[best_index]
    current_freq = f_res_guess
    print(f"Initial guess from amplitude sweep: {current_freq:.3f} Hz")

    # --- 2. Set the proportional gain.
    Kp = controller.gamma / (4 * np.pi)
    print(f"Using proportional gain: Kp = {Kp:.5f} Hz per radian")

    # --- 3. PLL loop.
    for i in range(max_iterations):
        controller.set_frequency(current_freq)
        error = controller.get_phase()
        if abs(error) < tol:
            print(f"PLL converged after {i} iterations with frequency {current_freq:.6f} Hz")
            break
        # Update the frequency using the error signal.
        current_freq = current_freq + Kp * error
        print(f"Iteration {i:3d}: Frequency = {current_freq:9.6f} Hz, Phase error = {error:9.6f} rad")
    else:
        print("Maximum iterations reached without full convergence in the PLL loop.")

    return current_freq

# =============================================================================
# 4. Main Routine
# =============================================================================


if __name__ == "__main__":
    # Set the damping constant (gamma) from prior calibration.
    gamma = 5  # Example value; use your system’s actual damping constant.
    
    # Create the controller interface.
    controller = ControllerTuningFork(gamma=gamma)
    
    # Run the PLL routine to estimate the resonance frequency.
    resonance_freq = find_resonance(controller)
    print(f"Final estimated resonance frequency: {resonance_freq:.6f} Hz")

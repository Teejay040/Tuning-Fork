#!/usr/bin/env python
# coding: utf-8

# In[29]:


pip install pyserial


# In[1]:


pip install keyboard


# In[7]:


pip install pipython


# In[6]:


#piezo
from pipython import GCSDevice
import time

class piezo():
    
    def __init__(self):
        self.pidevice = GCSDevice('E-625')
        self.pidevice.ConnectUSB("121019479")
        self.target = 'A'

    def absolute_voltage(self, voltage):
        self.pidevice.SVO(self.target, False)
        self.pidevice.SVA(self.target, voltage)

    def request_voltage(self):
        return self.pidevice.qVOL(self.target)


# In[7]:


#piezo
from pipython import GCSDevice
from threading import Thread
import threading
import time

class pi_e_625():
    
    def __init__(self):

        self.pidevice = GCSDevice('E-625')
        # Serial number to connect to can be read on device!
        self.pidevice.ConnectUSB("121019479")

#        Or use the dialog and you will read "E-816USB SN 121019479" 
#        self.pidevice.InterfaceSetupDlg(key='sample')

        self.stopMutex = threading.Lock()
        self._stop = True

        self.target = 'A'

        print("???")

    def servoloop(self,closed=False):
        
        self.pidevice.SVO(self.target,closed)


    def relative_voltage(self,voltage):

        self.pidevice.SVO(self.target,False)
        self.pidevice.SVR(self.target,voltage)

        
    def absolute_voltage(self,voltage):

        self.pidevice.SVO(self.target,False)
        self.pidevice.SVA(self.target,voltage)

    def request_voltage(self):

        return self.pidevice.qVOL(self.target)

    def thread_for_voltage(self,start,end,step,waittime):

        v = start

        while v < end:
            with self.stopMutex:
                if self._stop:
                    break
            self.absolute_voltage(v)
        
            v = v + step
            time.sleep(waittime)

        self.stop()

    def stop(self):
        # Must protect self._stop with a mutex because a secondary thread 
        # might try to access it at the same time.
        print("*")
        with self.stopMutex:
            if not self._stop:
                self._stop = True
                        
        
    def for_voltage(self,start,end,step,waittime):
        # Must protect self._stop with a mutex because a secondary thread 
        # might try to access it at the same time.
        # if a thread is already running do not start a second one!!!
        with self.stopMutex:
            if self._stop:
                self._stop = False
                ok_to_start = True
            else:
                ok_to_start = False

        if ok_to_start:                        

            self.for_task = Thread(target = self.thread_for_voltage, args =(start,end,step,waittime,))
    
            self.for_task.start()




if __name__ == '__main__':

    try:
        print("***")
        pz = pi_e_625()
        time.sleep(10)
        print(pz.request_voltage())
        pz.absolute_voltage(0.)
        time.sleep(1)
        print(pz.request_voltage())

        pz.for_voltage(0,1,1,1)

        door = True
        while door:
            with pz.stopMutex:
                door = not pz._stop
                time.sleep(.5)
            print(pz.request_voltage())
    finally:
        try:
            pz.stop()
        except:
            pass
        print("done")


# In[18]:


from pipython import GCSDevice
import time
import numpy as np

# Instellingen
CONTROLLER_NAME = "E-625"  # Naam van de controller
AXIS = 'Z'  # Asnaam
START_FREQ = 700  # Startfrequentie in Hz
END_FREQ = 800  # Eindfrequentie in Hz
STEP = 5  # Frequentiestap in Hz
DURATION = 2  # Duur per frequentie in seconden

def main():
    # Maak verbinding met de controller
    with GCSDevice(CONTROLLER_NAME) as controller:
        # Verbinden (pas het pad aan voor de seriële verbinding)
        controller.ConnectUSB('E-816USB SN 121019479')  # Vervang door de juiste poort
        print(f"Verbonden met: {controller.qIDN()}")

        # Controleer en initialiseer de Z-as
        try:
            # Vraag de status van alle assen op (als een lijst van statuswaarden)
            axis_status = controller.qSAI()  # Dit geeft de status van alle assen terug

            # Controleer de status van de Z-as (de Z-as heeft index 0 in de lijst)
            if axis_status[0] == 1:  # Controleer of de Z-as geactiveerd is
                controller.SVO(AXIS, 2)  # Schakel de servo in op de Z-as
                print(f"Servo geactiveerd op as {AXIS}")
            else:
                print(f"As {AXIS} is niet geactiveerd.")
        except Exception as e:
            print(f"Fout bij het controleren van de Z-as: {e}")

        # Voer de frequentiesweep uit
        for freq in np.arange(START_FREQ, END_FREQ + STEP, STEP):
            print(f"Aansturen met frequentie: {freq} Hz")
            amplitude = 10  # Pas de amplitude aan naar jouw systeem
            append = 0  # Voeg de golf niet toe aan een bestaande golf
            speedupdown = 1  # Versnellen en vertragen bij het opbouwen van de golf
            offset = 0  # Geen offset
            seglength = 100  # Stel de segmentlengte in (pas deze waarde naar wens aan)

            # Roep WAV_LIN aan met alle vereiste argumenten, inclusief 'seglength'
            try:
                controller.WAV_LIN(AXIS, freq, amplitude, append, speedupdown, offset, seglength)
                print(f"Golf gegenereerd voor frequentie {freq} Hz")
            except Exception as e:
                print(f"Fout bij het genereren van de golf voor {freq} Hz: {e}")
            
            time.sleep(DURATION)

        print("Sweep voltooid.")

if __name__ == "__main__":
    main()

